import cairo
from datetime import date, datetime

from gi.repository import Gtk, Gdk, GObject, Pango

from .eventeditor import EventEditor


BORDER_RADIUS = 5

EVENT_COLORS = [
    None,
    (0.23, 0.47, 0.81, 1),
    (0.17, 0.71, 0.52, 1),
    (0.72, 0.15, 0.15, 1),
]

EVENT_TITLES = [None, 'Práce', 'Dovolená', 'Nemoc']

MIN_DAY_HEIGHT = 40

MONTHS = (
    'Leden', 'Únor', 'Březen', 'Duben', 'Květen', 'Červen',
    'Červenec', 'Srpen', 'Září', 'Říjen', 'Listopad', 'Prosinec'
)

PI = 3.141592653589793


@Gtk.Template(filename='ui/workspace.ui')
class Workspace(Gtk.Stack):
    '''
    Widget představující hlavní pracovní plochu na vytváření a upravování
    odpracovaného času
    '''

    __gtype_name__ = 'Workspace'
    __gsignals__ = {
        'reload': (GObject.SIGNAL_RUN_FIRST, None, ())
    }

    _drawing_area = Gtk.Template.Child()
    _panel = Gtk.Template.Child()
    _label_left = Gtk.Template.Child()
    _label_right = Gtk.Template.Child()

    _date = (-1, -1)
    _day_count = 0
    _worker = -1
    _events = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.connect('realize', self._set_database)

    def _set_database(self, widget):
        self._database = self.get_toplevel().get_application().database

    def do_reload(self):
        '''Signál na aktualizaci widgetu podle jeho vlastností'''

        # Pokud nelze zobrazit editor
        if self._worker == -1 or self._date[1] == -1:
            self.set_visible_child_name('inactive')
            return

        # Jinak (jsou vybrány potřebné údaje)
        self.set_visible_child_name('active')

        worker = self._database.workers.get(
                self._worker, 'first_name, last_name').fetchone()
        self._label_left.set_text('{} {}'.format(*worker))
        self._label_right.set_text('{} {}'.format(
            MONTHS[self._date[1] - 1], self._date[0]))

        month = date(self._date[0], self._date[1], 1)
        next_month = month.replace(month=self._date[1]+1) if month.month < 12 \
            else date(self._date[0]+1, 1, 1)
        self._day_count = (next_month - month).days

        # Načtení událostí
        self._events = [[] for _ in range(self._day_count)]
        events = self._database.events.select(
            self._worker, *self._date, 'id, type, start, duration'
        )
        for event in events:
            d = datetime.fromisoformat(event[2])
            self._events[d.day-1].append([
                event[0], event[1], d.day, d.hour*60 + d.minute, event[3]
            ])

        # Překreslení
        self._drawing_area.queue_draw()
        self._panel.queue_draw()

    def update(self, obj, gparam):
        '''Nastaví vlastnost objektu'''

        prop = gparam.name
        value = obj.get_property(prop)

        if prop == 'current-worker':
            self._worker = value
        elif prop == 'current-date':
            self._date = value
        else:
            raise AttributeError('unknown property \'{}\''.format(prop))

        self.emit('reload')

    def update_event(self, status, event):
        '''Callback z EventEditoru pro upravení události'''

        if status == 'delete':
            self._database.events.remove(event[0])
            self._events[event[2]-1].remove(event)
        elif status == 'save':
            start = datetime(
                *self._date, event[2],
                *divmod(event[3], 60)
            )
            if event[0] == -1:
                uid = self._database.events.create(
                    typ=event[1],
                    start=start,
                    duration=event[4],
                    worker_id=self._worker
                )
                event[0] = uid
                self._events[event[2]-1].append(event)
            else:
                self._database.events.update(
                    uid=event[0],
                    typ=event[1],
                    start=start,
                    duration=event[4],
                )
        self._drawing_area.queue_draw()

    def _draw_event(self, ctx, event, day_height, hour_width):
        uid, typ, day, start, duration = event

        x = start * hour_width / 60
        y = (day - 1) * day_height + 1
        w = duration * hour_width / 60
        h = day_height - 3

        ctx.set_line_width(1)

        # Vypočítání souřadnic
        left = x + BORDER_RADIUS
        right = x + w - BORDER_RADIUS
        top = y + BORDER_RADIUS
        bottom = y + h - BORDER_RADIUS

        # Nakreslení rámečku
        ctx.set_source_rgba(*EVENT_COLORS[typ])
        ctx.new_path()
        ctx.arc(left,  top,    BORDER_RADIUS, PI, PI*3/2)
        ctx.arc(right, top,    BORDER_RADIUS, PI*3/2, 0)
        ctx.arc(right, bottom, BORDER_RADIUS, 0, PI/2)
        ctx.arc(left,  bottom, BORDER_RADIUS, PI/2, PI)
        ctx.close_path()
        ctx.fill()

        ctx.set_source_rgba(1, 1, 1, 0.8)

        # Zobrazení popisku
        ctx.save()
        ctx.select_font_face(
            'sans-serif', cairo.FontSlant.NORMAL, cairo.FontWeight.BOLD)
        text = EVENT_TITLES[typ]
        exts = ctx.text_extents(text)
        ctx.move_to(x + (w - exts.width) / 2, y + h/2 - 2)
        ctx.show_text(text)
        ctx.stroke()
        ctx.restore()

        # Zobrazení časového intervalu
        end = start + duration
        text = '{}:{:02d} \u2013 {}:{:02d}'.format(
            *divmod(start, 60), *divmod(end, 60))
        exts = ctx.text_extents(text)
        ctx.move_to(x + (w - exts.width) / 2, y + h/2 + 2 + exts.height)
        ctx.show_text(text)
        ctx.stroke()

    @Gtk.Template.Callback()
    def on_draw_numbers(self, area, ctx):
        # Získání velikostí
        area.set_size_request(50, self._day_count * MIN_DAY_HEIGHT)
        width = area.get_allocated_width()
        height = area.get_allocated_height()
        day_height = height / self._day_count

        # Načtení stylů
        style = area.get_style_context()
        state = area.get_state()

        fg_color = style.get_color(state)
        line_color = style.get_border_color(state)

        font = style.get_property(Gtk.STYLE_PROPERTY_FONT, state)
        font_size = font.get_size() / Pango.SCALE
        font_size_small = font_size * 0.6

        # Vykreslení čar
        ctx.save()
        ctx.set_line_width(0.25)
        ctx.set_source_rgba(*line_color)
        for i in range(1, self._day_count):
            y = i * day_height - 0.5
            ctx.move_to(0, y)
            ctx.line_to(width, y)
            ctx.stroke()
        ctx.restore()

        # Určení metrik
        ctx.select_font_face(
            'sans-serif', cairo.FontSlant.NORMAL, cairo.FontWeight.BOLD)
        ctx.set_font_size(font_size)
        box_number = ctx.text_extents('31')
        ctx.set_font_size(font_size_small + 8)
        box_name = ctx.text_extents('Sun')

        center = width / 2
        baseline = (box_number.height - box_name.height - day_height)/2

        # Vykreslení čísel dnů
        ctx.set_font_size(font_size)
        ctx.set_source_rgba(*fg_color)
        for i in range(1, self._day_count+1):
            y = i * day_height - 0.5
            text = str(i)
            extents = ctx.text_extents(text)

            ctx.move_to(center - extents.width/2, y + baseline)
            ctx.show_text(text)
            ctx.stroke()

        # Vykreslení jmen dnů
        ctx.set_font_size(font_size_small)
        fg_color.alpha = 0.7
        ctx.set_source_rgba(*fg_color)
        day = date(self._date[0], self._date[1], 1)
        for i in range(1, self._day_count+1):
            day = day.replace(day=i)
            y = i * day_height - 0.5
            text = day.strftime('%a')
            extents = ctx.text_extents(text)

            ctx.move_to(
                center - extents.width/2, y + baseline + box_name.height)
            ctx.show_text(text)
            ctx.stroke()

    @Gtk.Template.Callback()
    def on_draw(self, area, ctx):
        # Získání velikostí
        area.set_size_request(1200, self._day_count * MIN_DAY_HEIGHT)
        width = area.get_allocated_width()
        height = area.get_allocated_height()
        hour_width = width / 24
        day_height = height / self._day_count

        # Načtení vlastností z CSS stylů
        style = area.get_style_context()
        color = style.get_border_color(area.get_state())

        # Řádkování po dnech
        ctx.save()
        ctx.set_line_width(0.25)
        ctx.set_source_rgba(*color)
        for i in range(1, self._day_count):
            y = i * day_height - 0.5
            ctx.move_to(0, y)
            ctx.line_to(width, y)
            ctx.stroke()

        # Hodinové sloupečky
        ctx.set_dash((1.5, 5))
        for i in range(1, 24):
            x = i * hour_width - 0.5
            ctx.move_to(x, 0)
            ctx.line_to(x, height)
            ctx.stroke()
        ctx.restore()

        # Vykreslení událostí
        for events in self._events:
            for event in events:
                self._draw_event(ctx, event, day_height, hour_width)

    @Gtk.Template.Callback()
    def on_click(self, widget, event):
        # Získání rozměrů
        width = widget.get_allocated_width()
        height = widget.get_allocated_height()
        day_height = height / self._day_count
        hour_width = width / 24

        # Určení pozice kliknutí
        day = int(event.y // day_height + 1)
        hour = int(event.x // hour_width)
        t = hour*60 + 30

        # Nalezení odpovídající události nebo vytvoření nové
        event = None
        for e in self._events[day-1]:
            _, _, _, start, duration = e
            if (t - start) > 0 and (start + duration - t) > 0:
                event = e
                break
        else:
            event = [-1, 1, day, hour*60, 60]

        # Vyskakovací okno a jeho umístění
        rect = Gdk.Rectangle()
        rect.width = event[4] * hour_width / 60
        rect.height = day_height * 0.6
        rect.x = event[3] * hour_width / 60
        rect.y = (event[2] - 0.8) * day_height

        p = EventEditor(relative_to=widget, callback=self.update_event)
        p.set_pointing_to(rect)
        p.popup(event, self._events[day-1])

import cairo
from datetime import date

from gi.repository import Gtk, GObject, Pango


MIN_DAY_HEIGHT = 40


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

        month = date(self._date[0], self._date[1], 1)
        next_month = month.replace(month=self._date[1]+1) if month.month < 12 \
            else date(self._date[0]+1, 1, 1)
        self._day_count = (next_month - month).days
        self._label_right.set_text(month.strftime('%B %Y'))

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
        day_height = height / self._day_count
        hour_width = width / 24

        # Načtení vlastností z CSS stylů
        style = area.get_style_context()
        color = style.get_border_color(area.get_state())

        # Řádkování po dnech
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

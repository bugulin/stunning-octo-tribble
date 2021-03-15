from gi.repository import Gtk

MIN_DURATION = 10


@Gtk.Template(filename='ui/eventeditor.ui')
class EventEditor(Gtk.Popover):
    '''
    Vyskakovací okénko na úpravu údajů nějaké události.
    '''

    __gtype_name__ = 'EventEditor'

    _event_type = Gtk.Template.Child()
    _start_hours = Gtk.Template.Child()
    _start_minutes = Gtk.Template.Child()
    _stop_hours = Gtk.Template.Child()
    _stop_minutes = Gtk.Template.Child()

    _delete_button = Gtk.Template.Child()
    _save_button = Gtk.Template.Child()

    def __init__(self, *args, **kwargs):
        self._callback = kwargs.pop('callback')
        super().__init__(*args, **kwargs)

    def popup(self, event, day_schedule):
        self._event = event
        self._day_schedule = day_schedule

        # Načtení dat do widgetů
        start = event[3]
        self._start_hours.set_value(start // 60)
        self._start_minutes.set_value(start % 60)

        stop = start + event[4]
        self._stop_hours.set_value(stop // 60)
        self._stop_minutes.set_value(stop % 60)

        self._event_type.set_active_id(str(event[1]))

        # Deaktivace tlačítka 'Smazat'
        if event[0] == -1:
            self._delete_button.set_sensitive(False)

        super().popup()

    @Gtk.Template.Callback()
    def on_save(self, button):
        self._event[1] = int(self._event_type.get_active_id())
        self._event[3], self._event[4] = self._get_times()
        self._event[4] -= self._event[3]
        self._callback('save', self._event)
        self.destroy()

    @Gtk.Template.Callback()
    def on_delete(self, button):
        self._callback('delete', self._event)
        self.destroy()

    @Gtk.Template.Callback()
    def on_output(self, widget):
        value = widget.get_value()
        text = '{:02.0f}'.format(value)
        widget.set_text(text)
        return True

    def _get_times(self):
        start = int(self._start_hours.get_value() * 60
                    + self._start_minutes.get_value())
        stop = int(self._stop_hours.get_value() * 60
                   + self._stop_minutes.get_value())
        return start, stop

    def _on_spin_changed(self, widget_hours, widget_minutes):
        hour = int(widget_hours.get_value())
        minute = int(widget_minutes.get_value())
        adjustment = widget_minutes.get_adjustment()

        if minute > 59:
            widget_hours.set_value(hour + 1)
            widget_hours.get_adjustment().set_value(hour + 1)
            widget_minutes.set_value(minute - 60)
        elif minute < 0:
            widget_hours.set_value(hour - 1)
            widget_hours.get_adjustment().set_value(hour - 1)
            widget_minutes.set_value(minute + 60)

        adjustment.set_upper((1440, 59)[hour == 23])
        adjustment.set_lower((-1440, 0)[hour == 0])

    def _collide(self, interval):
        for e in self._day_schedule:
            if e is self._event:
                continue

            start = e[3]
            stop = start + e[4]
            if start <= interval[1] and interval[0] <= stop:
                return True

        return False

    @Gtk.Template.Callback()
    def on_value_changed(self, widget):
        if widget in (self._start_hours, self._start_minutes):
            self._on_spin_changed(self._start_hours, self._start_minutes)
        elif widget in (self._stop_hours, self._stop_minutes):
            self._on_spin_changed(self._stop_hours, self._stop_minutes)

        # Aktivace tlačítka 'Uložit'
        times = self._get_times()
        if (times[1] - times[0]) < MIN_DURATION or self._collide(times):
            self._save_button.set_sensitive(False)
        else:
            self._save_button.set_sensitive(True)

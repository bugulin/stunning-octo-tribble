from datetime import MINYEAR, MAXYEAR
from gi.repository import Gtk, GObject


@Gtk.Template(filename='ui/monthchooser.ui')
class MonthChooser(Gtk.Popover):
    '''Widget na výběr měsíce'''

    __gtype_name__ = 'MonthChooser'

    __gsignals__ = {
        'reload': (GObject.SIGNAL_RUN_FIRST, None, ())
    }

    _calendar = Gtk.Template.Child()
    _date = (-1, -1)  # GObject.Property: (year, month)

    @GObject.Property
    def current_date(self):
        return self._date

    @current_date.setter
    def current_date(self, value):
        self._date = value

    def run(self):
        self.popup()

    def do_reload(self):
        self._calendar.emit('month-changed')

    @Gtk.Template.Callback()
    def on_date_changed(self, calendar):
        date = calendar.get_date()
        if date.year < MINYEAR or date.year >= MAXYEAR:
            return calendar.select_month(
                date.month,
                MINYEAR + (date.year - MINYEAR) % (MAXYEAR - MINYEAR)
            )
        self.set_property('current-date', (date.year, date.month+1))

    @Gtk.Template.Callback()
    def close(self, widget):
        self.popdown()

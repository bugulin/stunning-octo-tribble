from gi.repository import Gtk, GObject


@Gtk.Template(filename='ui/monthchooser.ui')
class MonthChooser(Gtk.Popover):
    '''Widget na výběr měsíce'''

    __gtype_name__ = 'MonthChooser'

    _date = (0, 0)  # GObject.Property: (year, month)

    @GObject.Property
    def current_date(self):
        return self._date

    @current_date.setter
    def current_date(self, value):
        self._date = value

    def run(self):
        self.popup()

    @Gtk.Template.Callback()
    def on_date_changed(self, calendar):
        date = calendar.get_date()
        self.set_property('current_date', (date.year, date.month))

    @Gtk.Template.Callback()
    def close(self, widget):
        self.popdown()

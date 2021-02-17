from gi.repository import Gtk

from widgets.workersview import WorkersView  # Used in UI template


@Gtk.Template(filename='ui/window.ui')
class AppWindow(Gtk.ApplicationWindow):
    '''Hlavní okno aplikace'''

    __gtype_name__ = 'AppWindow'

    _button_save = Gtk.Template.Child()
    _viewport = Gtk.Template.Child()
    _workers_view = Gtk.Template.Child()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Setup bindings to database
        db = self.props.application.database
        self.update_status(db)
        db.connect('notify::saved', self.update_status)
        self._workers_view.connect_to(db.workers)

        self.show_all()

    def update_status(self, db, gparam=None):
        print('\x1b[1m[i]\x1b[0m', 'Database saved:', db.saved)
        self._button_save.set_sensitive(not db.saved)

    @Gtk.Template.Callback()
    def on_date_changed(self, calendar):
        date = calendar.get_date()
        # TODO: .set_property('date', (date.year, date.month))

    @Gtk.Template.Callback()
    def popup(self, widget):
        widget.popup()

    @Gtk.Template.Callback()
    def popdown(self, widget):
        widget.popdown()

    @Gtk.Template.Callback()
    def toggle_panel(self, button):
        self._workers_view.set_visible(button.get_active())

    @Gtk.Template.Callback()
    def on_destroy(self, widget):
        self.props.application.activate_action('quit')

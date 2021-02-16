from gi.repository import Gtk


@Gtk.Template(filename='ui/window.ui')
class AppWindow(Gtk.ApplicationWindow):
    '''Hlavní okno aplikace'''

    __gtype_name__ = 'AppWindow'

    _button_save = Gtk.Template.Child()
    _viewport = Gtk.Template.Child()
    _workers_panel = Gtk.Template.Child()
    _workers_view = Gtk.Template.Child()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Create a TreeViewColumn to display workers
        column = Gtk.TreeViewColumn('Seznam pracovníků')

        first_name = Gtk.CellRendererText(ellipsize_set=True, ellipsize=3)
        last_name = Gtk.CellRendererText(ellipsize_set=True, ellipsize=3)

        column.pack_start(first_name, True)
        column.pack_start(last_name, True)

        column.add_attribute(first_name, 'text', 1)
        column.add_attribute(last_name, 'text', 2)

        self._workers_view.append_column(column)
        column.set_sort_column_id(2)

        # Setup bindings to database
        db = self.props.application.database
        db.connect('notify::saved', self.update_status)
        self.update_status(db)
        self._workers_view.set_model(db.workers.store)

        self.show_all()

    def update_status(self, db, gparam=None):
        print('\x1b[1m[D]\x1b[0m', 'Database saved:', db.saved)
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
        self._workers_panel.set_visible(button.get_active())

    @Gtk.Template.Callback()
    def on_destroy(self, widget):
        self.props.application.activate_action('quit')

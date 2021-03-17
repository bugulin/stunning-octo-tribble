from gi.repository import Gtk

# Widgets used in UI template
from widgets.workersview import WorkersView
from widgets.monthchooser import MonthChooser
from widgets.workspace import Workspace


@Gtk.Template(filename='ui/window.ui')
class AppWindow(Gtk.ApplicationWindow):
    '''Hlavní okno aplikace'''

    __gtype_name__ = 'AppWindow'

    _button_save = Gtk.Template.Child()
    _month_chooser = Gtk.Template.Child()
    _workers_view = Gtk.Template.Child()
    _workspace = Gtk.Template.Child()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        db = self.props.application.database
        self.update_status(db)
        db.connect('notify::saved', self.update_status)

        self._workers_view.connect('notify::current-worker', self._workspace.update)
        self._month_chooser.connect('notify::current-date', self._workspace.update)
        self._month_chooser.emit('reload')

        self.show_all()

    def update_status(self, db, gparam=None):
        '''Deaktivuje tlačítko 'Uložit', pokud není co uložit'''

        self._button_save.set_sensitive(not db.saved)

    def reload_views(self):
        '''Vyvolá znovunačtení dat z databáze u všech zobrazení'''

        self._workers_view.emit('reload')
        self._workspace.emit('reload')

    def get_view(self):
        '''Vrátí aktuální pohled'''

        worker = self._workers_view.current_worker
        date = self._month_chooser.current_date
        return {'worker_id': worker, 'date': date}

    @Gtk.Template.Callback()
    def on_choose_month(self, widget):
        self._month_chooser.run()

    @Gtk.Template.Callback()
    def toggle_panel(self, button):
        self._workers_view.set_visible(button.get_active())

    @Gtk.Template.Callback()
    def on_destroy(self, widget):
        self.props.application.activate_action('quit')

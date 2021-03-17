from gi.repository import Gtk, GObject

from widgets.workerdialog import WorkerDialog


@Gtk.Template(filename='ui/workersview.ui')
class WorkersView(Gtk.Box):

    __gtype_name__ = 'WorkersView'

    __gsignals__ = {
        'reload': (GObject.SIGNAL_RUN_FIRST, None, ())
    }

    _button_edit = Gtk.Template.Child()
    _button_remove = Gtk.Template.Child()
    _selection = Gtk.Template.Child()
    _store = Gtk.Template.Child()

    current_worker = GObject.Property(type=int, default=-1)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.connect('realize', self._setup)

    def _setup(self, widget):
        db = self.get_toplevel().get_application().database
        self._workers = db.workers
        self._handler_id = self._selection.connect(
            'changed', self.on_selection_changed)
        self.emit('reload')

    def do_reload(self):
        with self._selection.handler_block(self._handler_id):
            self._store.clear()
            for worker in self._workers.all():
                self._store.append((worker[0], '{2} {1}'.format(*worker)))
        self._selection.emit('changed')

    @Gtk.Template.Callback()
    def on_create_worker(self, button):
        worker_dialog = WorkerDialog(
            transient_for=self.get_toplevel(),
            title='Vytvořit nový záznam',
        )

        response, data = worker_dialog.run()
        if response == Gtk.ResponseType.OK:
            uid = self._workers.create(**data)
            worker = self._workers.get(uid).fetchone()
            treeiter = self._store.append(
                (worker[0], '{2} {1}'.format(*worker)))
            self._selection.select_iter(treeiter)

    @Gtk.Template.Callback()
    def on_edit_worker(self, button):
        worker_dialog = WorkerDialog(
            transient_for=self.get_toplevel(),
            title='Upravit záznam',
        )

        uid = self.current_worker
        model, treeiter = self._selection.get_selected()

        worker = self._workers.get(uid, 'first_name, last_name').fetchone()
        response, data = worker_dialog.run(
            first_name=worker[0],
            last_name=worker[1]
        )
        if response == Gtk.ResponseType.OK:
            self._workers.update(uid, **data)
            worker = self._workers.get(uid).fetchone()
            model.set(treeiter, (0, 1), (worker[0], '{2} {1}'.format(*worker)))

    @Gtk.Template.Callback()
    def on_remove_worker(self, button):
        self._workers.remove(self.current_worker)
        _, treeiter = self._selection.get_selected()
        self._store.remove(treeiter)
        self._selection.unselect_all()
        self.current_worker = -1

    def on_selection_changed(self, selection):
        model, treeiter = selection.get_selected()
        if treeiter is None:
            self.current_worker = -1
            self._button_edit.set_sensitive(False)
            self._button_remove.set_sensitive(False)
        else:
            self.current_worker = model[treeiter][0]
            self._button_edit.set_sensitive(True)
            self._button_remove.set_sensitive(True)
            self._selection.get_tree_view().scroll_to_cell(
                model.get_path(treeiter))

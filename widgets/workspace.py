from gi.repository import Gtk, GObject


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
    _month_label = Gtk.Template.Child()
    _worker_name = Gtk.Template.Child()

    _date = (-1, -1)
    _worker = -1

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.connect('realize', self._set_database)

    def _set_database(self, widget):
        self._database = self.get_toplevel().get_application().database

    def do_reload(self):
        if self._worker == -1 or self._date[1] == -1:
            self.set_visible_child_name('inactive')
            return

        self.set_visible_child_name('active')
        worker = self._database.workers.get(
                self._worker, 'first_name, last_name').fetchone()
        self._worker_name.set_text('{} {}'.format(*worker))
        self._month_label.set_text(
                '{}/{}'.format(self._date[1]+1, self._date[0]))

    def update(self, obj, gparam):
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
    def on_draw(self, area, context):
        pass

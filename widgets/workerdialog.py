from gi.repository import Gtk


@Gtk.Template(filename='ui/workerdialog.ui')
class WorkerDialog(Gtk.Dialog):
    '''Dialogové okno na úpravu pracovníka'''

    __gtype_name__ = 'WorkerDialog'

    _first_name = Gtk.Template.Child()
    _last_name = Gtk.Template.Child()

    def present(self):
        response = self.run()
        data = {
            'first_name': self._first_name.get_text(),
            'last_name': self._last_name.get_text(),
        }
        self.destroy()

        return response, data

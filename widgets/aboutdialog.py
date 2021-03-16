from gi.repository import Gtk

@Gtk.Template(filename='ui/aboutdialog.ui')
class AboutDialog(Gtk.AboutDialog):
    '''Dialogové okno zobrazující základní informace o aplikaci'''

    __gtype_name__ = 'AboutDialog'

    @Gtk.Template.Callback()
    def on_response(self, widget, response):
        self.destroy()

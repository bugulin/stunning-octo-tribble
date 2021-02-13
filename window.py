from gi.repository import Gtk


@Gtk.Template(filename='ui/window.ui')
class AppWindow(Gtk.ApplicationWindow):

    __gtype_name__ = 'AppWindow'

    _viewport = Gtk.Template.Child()
    _workers_panel = Gtk.Template.Child()
    _workers_view = Gtk.Template.Child()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.show_all()

    @Gtk.Template.Callback()
    def on_date_changed(self, calendar):
        date = calendar.get_date()
        self.props.application.set_property('date', (date.year, date.month))

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
        self.props.application.quit()

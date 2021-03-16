from datetime import datetime

from gi.repository import Gtk, GLib


@Gtk.Template(filename='modules/exporter.ui')
class Exporter(Gtk.Dialog):
    '''Dialog pro exportování dat'''

    __gtype_name__ = 'Exporter'

    _ok_button = Gtk.Template.Child()
    _filename = Gtk.Template.Child()
    _progress = Gtk.Template.Child()

    def __init__(self, *args, **kwargs):
        self._worker_id = kwargs.pop('worker_id')
        self._date = kwargs.pop('date')

        super().__init__(*args, **kwargs)

        self._ok_button.set_sensitive(False)

    def _set_progress(self, fraction, text=None):
        if text is None:
            text = '{:2.0f} %'.format(fraction*100)

        self._progress.set_fraction(fraction)
        self._progress.set_text(text)

    def to_csv(self, filename):
        self._ok_button.set_sensitive(False)
        self._ok_button.set_label('Probíhá export')

        db = self.get_transient_for().get_application().database
        events = sorted(db.events.select(
            self._worker_id, *self._date, 'start, duration, type'))

        try:
            self._set_progress(0, 'Probíhá export...')
            f = open(filename, 'w')
            f.write('Datum,Čas,Délka,Typ\n')

            for i, event in enumerate(events):
                start = datetime.fromisoformat(event[0])
                f.write('{},{},{:02d}:{:02d},{}\n'.format(
                    start.strftime('%Y-%m-%d'), start.strftime('%H:%M'),
                    *divmod(event[1], 60), event[2],
                ))

                self._set_progress((i+1) / len(events))
                yield True

            f.close()
            self._set_progress(1, 'Hotovo!')

        except Exception as error:
            self._set_progress(0, 'Nastala chyba :(')
            print(error)

        self._ok_button.set_sensitive(True)
        self._ok_button.set_label('Exportovat')
        yield False

    @Gtk.Template.Callback()
    def on_file_choose(self, button):
        dialog = Gtk.FileChooserDialog(
            parent=self,
            action=Gtk.FileChooserAction.SAVE
        )
        dialog.add_buttons(
            Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
            Gtk.STOCK_OK, Gtk.ResponseType.OK,
        )

        filter1 = Gtk.FileFilter()
        filter1.set_name('CSV soubory')
        filter1.add_mime_type('text/csv')
        dialog.add_filter(filter1)

        filter2 = Gtk.FileFilter()
        filter2.set_name('Všechny soubory')
        filter2.add_pattern('*')
        dialog.add_filter(filter2)

        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            self._filename.set_text(dialog.get_filename())
            self._ok_button.set_sensitive(True)
        dialog.destroy()

    @Gtk.Template.Callback()
    def on_response(self, widget, response):
        if response == Gtk.ResponseType.OK:
            filename = self._filename.get_text()
            task = self.to_csv(filename)
            GLib.idle_add(next, task)
        else:
            self.destroy()

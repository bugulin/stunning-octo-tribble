#!/usr/bin/env python3
import sys

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GObject, GLib, Gio

from window import AppWindow
from widgets.aboutdialog import AboutDialog


class OctoTribble(Gtk.Application):

    _date = (0, 0)  # (year, month)
    _worker = None

    def __init__(self, *args, **kwargs):
        super().__init__(
            *args,
            application_id='cz.bugulin.stunning_octo_tribble',
            #flags=...,
            **kwargs
        )

        self._window = None

    @GObject.Property
    def date(self):
        return self._date

    @date.setter
    def date(self, value):
        self._date = value

    @GObject.Property
    def worker(self):
        return self._worker

    @worker.setter
    def worker(self, value):
        self._worker = value

    def do_startup(self):
        Gtk.Application.do_startup(self)

        about = Gio.SimpleAction.new('about', None)
        about.connect('activate', self.on_about)
        self.add_action(about)

    def do_activate(self):
        if not self._window:
            self._window = AppWindow(application=self)

        self._window.present()

    def on_about(self, action, param):
        about_dialog = AboutDialog(transient_for=self._window)
        about_dialog.present()


if __name__ == '__main__':
    app = OctoTribble()
    app.run(sys.argv)

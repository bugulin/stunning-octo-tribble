#!/usr/bin/env python3
import os
import sys

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, Gio

from database import Database
from managers import WorkerManager, EventManager

from window import AppWindow
from widgets.aboutdialog import AboutDialog
from modules.exporter import Exporter


DB_PATH = 'db.sqlite3'


class OctoTribble(Gtk.Application):

    def __init__(self, *args, **kwargs):
        super().__init__(
            *args,
            application_id='cz.bugulin.stunning_octo_tribble',
            #flags=...,
            **kwargs
        )

        self._window = None
        self.database = None

    def _setup_database(self):
        create_schemes = False
        if not os.path.isfile(DB_PATH):
            create_schemes = True

        self.database = Database('db.sqlite3')
        self.database.register(WorkerManager)
        self.database.register(EventManager)

        # Vytvoření tabulek, pokud neexistují
        if create_schemes:
            self.database.create_schemes()

    def do_startup(self):
        Gtk.Application.do_startup(self)

        action_entries = [
            ('about', self.on_about),
            ('export', self.on_export),
            ('reload', self.on_reload),
            ('save', self.on_save),
            ('quit', self.on_quit),
        ]

        for action, callback in action_entries:
            sa = Gio.SimpleAction.new(action, None)
            sa.connect('activate', callback)
            self.add_action(sa)

        css = Gtk.CssProvider()
        css.load_from_path('data/theme.css')
        style = Gtk.StyleContext()
        style.add_provider_for_screen(
            Gdk.Screen.get_default(), css, Gtk.STYLE_PROVIDER_PRIORITY_USER)

    def do_activate(self):
        if not self._window:
            self._setup_database()
            self._window = AppWindow(application=self)

        self._window.present()

    def on_about(self, action, param):
        about_dialog = AboutDialog(transient_for=self._window)
        about_dialog.present()

    def on_export(self, action, param):
        export_dialog = Exporter(
            transient_for=self._window, **self._window.get_view())
        export_dialog.present()

    def on_reload(self, action, param):
        self.database.rollback()
        self._window.reload_views()

    def on_save(self, action, param):
        self.database.save()

    def on_quit(self, action, param):
        self.database.quit()
        self.quit()


if __name__ == '__main__':
    app = OctoTribble()
    app.run(sys.argv)

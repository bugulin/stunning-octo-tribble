#!/usr/bin/env python3
import sys

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gio

from database import Database
from managers import WorkerManager

from window import AppWindow
from widgets.aboutdialog import AboutDialog
from widgets.workerdialog import WorkerDialog


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

    def setup_database(self):
        self.database = Database('db.sqlite3')
        self.database.register(WorkerManager)

    def do_startup(self):
        Gtk.Application.do_startup(self)

        action_entries = [
            ('about', self.on_about),
            ('save', self.on_save),
            ('quit', self.on_quit),
            ('create_worker', self.on_create_worker),
        ]

        for action, callback in action_entries:
            sa = Gio.SimpleAction.new(action, None)
            sa.connect('activate', callback)
            self.add_action(sa)

    def do_activate(self):
        if not self._window:
            self.setup_database()
            self._window = AppWindow(application=self)

        self._window.present()

    def on_about(self, action, param):
        about_dialog = AboutDialog(transient_for=self._window)
        about_dialog.present()

    def on_save(self, action, param):
        self.database.save()

    def on_quit(self, action, param):
        self.database.quit()
        self.quit()

    def on_create_worker(self, action, param):
        worker_dialog = WorkerDialog(
            transient_for=self._window, title='Vytvořit nový záznam'
        )
        response, worker = worker_dialog.present()
        if response == Gtk.ResponseType.OK:
            self.database.workers.create(**worker)


if __name__ == '__main__':
    app = OctoTribble()
    app.run(sys.argv)

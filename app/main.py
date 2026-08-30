import sys
import os
import gi

gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Adw, Gio, GLib

from app.ui.window import NotesWindow
from app.db import Database

class NotesApp(Adw.Application):
    def __init__(self):
        super().__init__(application_id='com.example.Notes',
                         flags=Gio.ApplicationFlags.FLAGS_NONE)
        
        # Determine data directory for SQLite DB
        data_dir = GLib.get_user_data_dir()
        app_data_dir = os.path.join(data_dir, 'com.example.Notes')
        db_path = os.path.join(app_data_dir, 'notes.db')
        
        self.db = Database(db_path)
        self.window = None

    def do_activate(self):
        if not self.window:
            self.window = NotesWindow(application=self, db=self.db)
        self.window.present()

def main():
    app = NotesApp()
    return app.run(sys.argv)

if __name__ == '__main__':
    sys.exit(main())

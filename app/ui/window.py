import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Gtk, Adw, Gio, GLib

from app.ui.sidebar import Sidebar
from app.ui.note_list import NoteList
from app.ui.editor import Editor

class NotesWindow(Adw.ApplicationWindow):
    def __init__(self, application, db, **kwargs):
        super().__init__(application=application, **kwargs)
        self.db = db
        self.set_title("Notlar")
        self.set_default_size(900, 600)
        
        self.build_ui()
        self.load_initial_data()

    def build_ui(self):
        # Toast overlay for notifications
        self.toast_overlay = Adw.ToastOverlay()
        self.set_content(self.toast_overlay)

        # Split views
        self.inner_split_view = Adw.OverlaySplitView()
        self.outer_split_view = Adw.OverlaySplitView()
        
        # 3 Panel Layout: Sidebar (Folders) | Note List | Editor
        self.editor_panel = Editor(self.db, self)
        self.note_list_panel = NoteList(self.db, self)
        self.sidebar_panel = Sidebar(self.db, self)
        
        # Inner split view (Note List | Editor)
        self.inner_split_view.set_sidebar(self.note_list_panel)
        self.inner_split_view.set_content(self.editor_panel)
        self.inner_split_view.set_sidebar_width_fraction(0.35)
        self.inner_split_view.set_min_sidebar_width(250)
        
        # Outer split view (Sidebar | Inner Split View)
        self.outer_split_view.set_sidebar(self.sidebar_panel)
        self.outer_split_view.set_content(self.inner_split_view)
        self.outer_split_view.set_sidebar_width_fraction(0.25)
        self.outer_split_view.set_min_sidebar_width(200)
        
        # Breakpoints for responsive design
        bp_outer = Adw.Breakpoint(condition=Adw.BreakpointCondition.parse("max-width: 800px"))
        bp_outer.add_setter(self.outer_split_view, "collapsed", True)
        self.add_breakpoint(bp_outer)

        bp_inner = Adw.Breakpoint(condition=Adw.BreakpointCondition.parse("max-width: 600px"))
        bp_inner.add_setter(self.inner_split_view, "collapsed", True)
        self.add_breakpoint(bp_inner)

        self.toast_overlay.set_child(self.outer_split_view)
        
        # Keyboard shortcuts
        self.setup_actions()
        
    def setup_actions(self):
        action_new = Gio.SimpleAction.new("new_note", None)
        action_new.connect("activate", self.on_new_note_action)
        self.add_action(action_new)
        self.get_application().set_accels_for_action("win.new_note", ["<Ctrl>n"])
        
    def on_new_note_action(self, action, param):
        self.note_list_panel.create_new_note()

    def load_initial_data(self):
        self.sidebar_panel.load_folders()
        self.note_list_panel.load_notes()

    def show_toast(self, message):
        toast = Adw.Toast.new(message)
        self.toast_overlay.add_toast(toast)
        
    def on_folder_selected(self, folder_id):
        self.note_list_panel.load_notes(folder_id=folder_id)
        if self.outer_split_view.get_collapsed():
            self.outer_split_view.set_show_sidebar(False)

    def on_note_selected(self, note_id):
        self.editor_panel.load_note(note_id)
        if self.inner_split_view.get_collapsed():
            self.inner_split_view.set_show_sidebar(False)
            
    def on_note_deleted(self, note_id):
        self.editor_panel.clear()
        self.note_list_panel.load_notes()
        self.show_toast("Not silindi.")
        
    def on_note_saved(self):
        self.note_list_panel.refresh_current_list()

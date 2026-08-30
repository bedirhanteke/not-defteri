import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Gtk, Adw, Pango, GLib

class NoteList(Gtk.Box):
    def __init__(self, db, window):
        super().__init__(orientation=Gtk.Orientation.VERTICAL)
        self.db = db
        self.window = window
        self.add_css_class("background")
        self.current_folder_id = None
        
        # Header bar
        self.header = Adw.HeaderBar()
        self.header.set_show_title(False)
        self.header.set_show_end_title_buttons(False)
        
        # Show sidebar button (for small screens)
        show_sidebar_btn = Gtk.Button(icon_name="go-previous-symbolic")
        show_sidebar_btn.set_tooltip_text("Klasörleri Göster")
        self.window.outer_split_view.bind_property(
            "collapsed", show_sidebar_btn, "visible", 
            gi.repository.GObject.BindingFlags.SYNC_CREATE)
        show_sidebar_btn.connect("clicked", lambda x: self.window.outer_split_view.set_show_sidebar(True))
        self.header.pack_start(show_sidebar_btn)
        
        # New note button
        add_btn = Gtk.Button(icon_name="document-new-symbolic")
        add_btn.set_tooltip_text("Yeni Not Ekle")
        add_btn.connect("clicked", lambda x: self.create_new_note())
        self.header.pack_end(add_btn)

        self.append(self.header)

        # Search bar
        self.search_entry = Gtk.SearchEntry()
        self.search_entry.set_margin_start(12)
        self.search_entry.set_margin_end(12)
        self.search_entry.set_margin_top(6)
        self.search_entry.set_margin_bottom(6)
        self.search_entry.connect("search-changed", self.on_search_changed)
        self.append(self.search_entry)

        # ListBox for notes
        self.listbox = Gtk.ListBox()
        self.listbox.set_selection_mode(Gtk.SelectionMode.SINGLE)
        self.listbox.connect("row-activated", self.on_row_activated)
        self.listbox.add_css_class("boxed-list")
        self.listbox.set_margin_start(12)
        self.listbox.set_margin_end(12)
        self.listbox.set_margin_top(6)
        self.listbox.set_margin_bottom(6)
        
        scrolled = Gtk.ScrolledWindow()
        scrolled.set_vexpand(True)
        scrolled.set_child(self.listbox)
        self.append(scrolled)
        
        self.search_timeout = 0

    def load_notes(self, folder_id=None, search_query=None):
        if folder_id is not False:
            self.current_folder_id = folder_id

        # Clear list
        while child := self.listbox.get_first_child():
            self.listbox.remove(child)
            
        notes = self.db.get_notes(self.current_folder_id, search_query)
        
        for note in notes:
            row = Gtk.ListBoxRow()
            
            vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=4)
            vbox.set_margin_start(12)
            vbox.set_margin_end(12)
            vbox.set_margin_top(12)
            vbox.set_margin_bottom(12)
            
            title_lbl = Gtk.Label(label=note['title'] or "İsimsiz Not", xalign=0)
            title_lbl.add_css_class("heading")
            title_lbl.set_ellipsize(Pango.EllipsizeMode.END)
            
            if note['is_pinned']:
                hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
                pin_icon = Gtk.Image.new_from_icon_name("view-pin-symbolic")
                hbox.append(pin_icon)
                hbox.append(title_lbl)
                vbox.append(hbox)
            else:
                vbox.append(title_lbl)
                
            # preview
            preview_text = note['content'][:100].replace('\n', ' ') + "..." if len(note['content']) > 100 else note['content'].replace('\n', ' ')
            preview_lbl = Gtk.Label(label=preview_text, xalign=0)
            preview_lbl.add_css_class("dim-label")
            preview_lbl.set_ellipsize(Pango.EllipsizeMode.END)
            vbox.append(preview_lbl)
            
            row.set_child(vbox)
            row.note_id = note['id']
            self.listbox.append(row)

        if notes:
            first_row = self.listbox.get_row_at_index(0)
            if first_row:
                self.listbox.select_row(first_row)
                self.window.on_note_selected(first_row.note_id)
        else:
            self.window.editor_panel.clear()

    def refresh_current_list(self):
        self.load_notes(folder_id=False, search_query=self.search_entry.get_text())

    def on_row_activated(self, listbox, row):
        self.window.on_note_selected(row.note_id)

    def create_new_note(self):
        note_id = self.db.add_note("Yeni Not", "", self.current_folder_id)
        self.refresh_current_list()
        self.window.on_note_selected(note_id)

    def on_search_changed(self, entry):
        if self.search_timeout:
            GLib.source_remove(self.search_timeout)
        self.search_timeout = GLib.timeout_add(300, self.do_search)

    def do_search(self):
        self.search_timeout = 0
        query = self.search_entry.get_text()
        self.load_notes(folder_id=False, search_query=query)
        return False

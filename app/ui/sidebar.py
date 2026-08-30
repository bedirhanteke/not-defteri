import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Gtk, Adw

class Sidebar(Gtk.Box):
    def __init__(self, db, window):
        super().__init__(orientation=Gtk.Orientation.VERTICAL)
        self.db = db
        self.window = window
        self.add_css_class("background")
        
        # Header bar
        self.header = Adw.HeaderBar()
        self.header.set_show_title(False)
        self.header.set_show_end_title_buttons(False)
        self.append(self.header)

        # Title
        title_label = Gtk.Label(label="Klasörler")
        title_label.add_css_class("title-1")
        title_label.set_margin_top(12)
        title_label.set_margin_bottom(12)
        
        # ListBox for folders
        self.listbox = Gtk.ListBox()
        self.listbox.set_selection_mode(Gtk.SelectionMode.SINGLE)
        self.listbox.connect("row-activated", self.on_row_activated)
        self.listbox.add_css_class("navigation-sidebar")
        
        scrolled = Gtk.ScrolledWindow()
        scrolled.set_vexpand(True)
        scrolled.set_child(self.listbox)
        
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        box.append(title_label)
        box.append(scrolled)
        self.append(box)
        
        # Add folder button
        add_btn = Gtk.Button(icon_name="list-add-symbolic")
        add_btn.set_tooltip_text("Yeni Klasör Ekle")
        add_btn.connect("clicked", self.on_add_folder)
        self.header.pack_start(add_btn)

    def load_folders(self):
        # Clear list
        while child := self.listbox.get_first_child():
            self.listbox.remove(child)
            
        # Default "All Notes" item
        all_row = Gtk.ListBoxRow()
        all_lbl = Gtk.Label(label="Tüm Notlar", xalign=0)
        all_lbl.set_margin_start(12)
        all_lbl.set_margin_end(12)
        all_lbl.set_margin_top(8)
        all_lbl.set_margin_bottom(8)
        all_row.set_child(all_lbl)
        all_row.folder_id = None
        self.listbox.append(all_row)
        
        # Load from DB
        folders = self.db.get_folders()
        for f in folders:
            row = Gtk.ListBoxRow()
            lbl = Gtk.Label(label=f['name'], xalign=0)
            lbl.set_margin_start(12)
            lbl.set_margin_end(12)
            lbl.set_margin_top(8)
            lbl.set_margin_bottom(8)
            row.set_child(lbl)
            row.folder_id = f['id']
            self.listbox.append(row)

    def on_row_activated(self, listbox, row):
        self.window.on_folder_selected(row.folder_id)

    def on_add_folder(self, btn):
        dialog = Adw.MessageDialog(heading="Yeni Klasör", body="Klasör adını girin:")
        entry = Gtk.Entry()
        dialog.set_extra_child(entry)
        dialog.add_response("cancel", "İptal")
        dialog.add_response("add", "Ekle")
        dialog.set_response_appearance("add", Adw.ResponseAppearance.SUGGESTED)
        
        def on_response(dialog, response):
            if response == "add":
                name = entry.get_text().strip()
                if name:
                    if self.db.add_folder(name):
                        self.load_folders()
                    else:
                        self.window.show_toast("Bu klasör zaten var.")
        
        dialog.connect("response", on_response)
        dialog.set_transient_for(self.window)
        dialog.present()

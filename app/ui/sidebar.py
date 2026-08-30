import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Gtk, Adw, Gdk

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
        all_row.folder_name = "Tüm Notlar"
        self.listbox.append(all_row)
        
        # Load from DB
        folders = self.db.get_folders()
        for f in folders:
            row = Gtk.ListBoxRow()
            
            hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
            lbl = Gtk.Label(label=f['name'], xalign=0)
            lbl.set_hexpand(True)
            lbl.set_margin_start(12)
            lbl.set_margin_end(6)
            lbl.set_margin_top(8)
            lbl.set_margin_bottom(8)
            hbox.append(lbl)
            
            # Options button (three dots)
            opt_btn = Gtk.Button(icon_name="view-more-symbolic")
            opt_btn.add_css_class("flat")
            opt_btn.set_valign(Gtk.Align.CENTER)
            opt_btn.set_tooltip_text("Klasör Seçenekleri")
            opt_btn.connect("clicked", lambda b, r=row: self.show_folder_menu(r, b))
            hbox.append(opt_btn)
            
            row.set_child(hbox)
            row.folder_id = f['id']
            row.folder_name = f['name']
            
            # Attach right-click gesture for context menu
            gesture = Gtk.GestureClick()
            gesture.set_button(Gdk.BUTTON_SECONDARY)  # 3: Right click
            gesture.connect("pressed", lambda g, n, x, y, r=row: self.show_folder_menu(r, r))
            hbox.add_controller(gesture)
            
            self.listbox.append(row)

    def on_row_activated(self, listbox, row):
        self.window.on_folder_selected(row.folder_id)

    def show_folder_menu(self, row, target_widget):
        if row.folder_id is None:
            return

        popover = Gtk.Popover()
        row.popover = popover  # Keep Python ref to prevent GC cleanup!
        popover.set_parent(target_widget)

        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=2)
        vbox.set_margin_start(6)
        vbox.set_margin_end(6)
        vbox.set_margin_top(6)
        vbox.set_margin_bottom(6)

        rename_btn = Gtk.Button(label="Yeniden Adlandır")
        rename_btn.add_css_class("flat")
        rename_btn.connect("clicked", lambda b: (popover.popdown(), self.on_rename_folder(row)))
        vbox.append(rename_btn)

        delete_btn = Gtk.Button(label="Klasörü Sil")
        delete_btn.add_css_class("flat")
        delete_btn.add_css_class("destructive-action")
        delete_btn.connect("clicked", lambda b: (popover.popdown(), self.on_delete_folder(row)))
        vbox.append(delete_btn)

        popover.set_child(vbox)
        popover.popup()

    def on_add_folder(self, btn):
        dialog = Adw.MessageDialog(heading="Yeni Klasör", body="Klasör adını girin:")
        entry = Gtk.Entry()
        entry.set_placeholder_text("Klasör Adı...")
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
                        self.window.show_toast(f"'{name}' klasörü oluşturuldu.")
                    else:
                        self.window.show_toast("Bu isimde bir klasör zaten var.")
        
        dialog.connect("response", on_response)
        dialog.set_transient_for(self.window)
        dialog.present()

    def on_rename_folder(self, row):
        dialog = Adw.MessageDialog(heading="Klasörü Yeniden Adlandır", body="Yeni klasör adını girin:")
        entry = Gtk.Entry()
        entry.set_text(row.folder_name)
        dialog.set_extra_child(entry)
        dialog.add_response("cancel", "İptal")
        dialog.add_response("save", "Kaydet")
        dialog.set_response_appearance("save", Adw.ResponseAppearance.SUGGESTED)
        
        def on_response(dialog, response):
            if response == "save":
                new_name = entry.get_text().strip()
                if new_name and new_name != row.folder_name:
                    if self.db.rename_folder(row.folder_id, new_name):
                        self.load_folders()
                        self.window.show_toast("Klasör adı değiştirildi.")
                    else:
                        self.window.show_toast("Bu isimde bir klasör zaten var.")
        
        dialog.connect("response", on_response)
        dialog.set_transient_for(self.window)
        dialog.present()

    def on_delete_folder(self, row):
        dialog = Adw.MessageDialog(
            heading="Klasörü Sil",
            body=f"'{row.folder_name}' klasörünü silmek istediğinize emin misiniz?\nNotlar silinmez, Tüm Notlar'a taşınır."
        )
        dialog.add_response("cancel", "İptal")
        dialog.add_response("delete", "Sil")
        dialog.set_response_appearance("delete", Adw.ResponseAppearance.DESTRUCTIVE)
        
        def on_response(dialog, response):
            if response == "delete":
                self.db.delete_folder(row.folder_id)
                self.load_folders()
                self.window.show_toast("Klasör silindi.")
                
        dialog.connect("response", on_response)
        dialog.set_transient_for(self.window)
        dialog.present()

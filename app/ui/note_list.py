import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Gtk, Adw, Pango, GLib, Gdk

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
        folder_changed = False
        if folder_id is not False:
            if self.current_folder_id != folder_id:
                folder_changed = True
            self.current_folder_id = folder_id

        # Clear list
        while child := self.listbox.get_first_child():
            self.listbox.remove(child)
            
        notes = self.db.get_notes(self.current_folder_id, search_query)
        
        current_selected_id = self.window.editor_panel.current_note_id
        selected_row = None

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
            row.note_title = note['title']
            
            # Attach right-click gesture for context menu
            gesture = Gtk.GestureClick()
            gesture.set_button(Gdk.BUTTON_SECONDARY)  # 3: Right click
            gesture.connect("pressed", lambda g, n, x, y, r=row: self.show_note_menu(r, r))
            vbox.add_controller(gesture)
            
            self.listbox.append(row)
            if current_selected_id and note['id'] == current_selected_id:
                selected_row = row

        if not folder_changed and selected_row:
            self.listbox.select_row(selected_row)
        elif notes:
            first_row = self.listbox.get_row_at_index(0)
            if first_row:
                self.listbox.select_row(first_row)
                self.window.on_note_selected(first_row.note_id)
        else:
            self.window.editor_panel.clear()

    def show_note_menu(self, row, target_widget):
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
        rename_btn.connect("clicked", lambda b: (popover.popdown(), self.on_rename_note(row)))
        vbox.append(rename_btn)

        pin_btn = Gtk.Button(label="Sabitle / Sabitlemeyi Kaldır")
        pin_btn.add_css_class("flat")
        pin_btn.connect("clicked", lambda b: (popover.popdown(), self.on_toggle_pin(row)))
        vbox.append(pin_btn)

        delete_btn = Gtk.Button(label="Notu Sil")
        delete_btn.add_css_class("flat")
        delete_btn.add_css_class("destructive-action")
        delete_btn.connect("clicked", lambda b: (popover.popdown(), self.on_delete_note(row)))
        vbox.append(delete_btn)

        popover.set_child(vbox)
        popover.popup()

    def on_rename_note(self, row):
        note = self.db.get_note(row.note_id)
        if not note:
            return
        dialog = Adw.MessageDialog(heading="Not Başlığını Değiştir", body="Yeni not başlığını girin:")
        entry = Gtk.Entry()
        entry.set_text(note['title'] or "")
        dialog.set_extra_child(entry)
        dialog.add_response("cancel", "İptal")
        dialog.add_response("save", "Kaydet")
        dialog.set_response_appearance("save", Adw.ResponseAppearance.SUGGESTED)

        def on_response(dialog, response):
            if response == "save":
                new_title = entry.get_text().strip()
                if new_title:
                    self.db.update_note(row.note_id, new_title, note['content'])
                    self.refresh_current_list()
                    if self.window.editor_panel.current_note_id == row.note_id:
                        self.window.editor_panel.load_note(row.note_id)
                    self.window.show_toast("Not başlığı güncellendi.")

        dialog.connect("response", on_response)
        dialog.set_transient_for(self.window)
        dialog.present()

    def on_toggle_pin(self, row):
        self.db.toggle_pin(row.note_id)
        self.refresh_current_list()

    def on_delete_note(self, row):
        dialog = Adw.MessageDialog(heading="Notu Sil", body="Bu notu silmek istediğinize emin misiniz?")
        dialog.add_response("cancel", "İptal")
        dialog.add_response("delete", "Sil")
        dialog.set_response_appearance("delete", Adw.ResponseAppearance.DESTRUCTIVE)

        def on_response(dialog, response):
            if response == "delete":
                self.db.delete_note(row.note_id)
                self.window.on_note_deleted(row.note_id)

        dialog.connect("response", on_response)
        dialog.set_transient_for(self.window)
        dialog.present()

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

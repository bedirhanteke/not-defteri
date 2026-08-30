import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Gtk, Adw, GLib

class Editor(Gtk.Box):
    def __init__(self, db, window):
        super().__init__(orientation=Gtk.Orientation.VERTICAL)
        self.db = db
        self.window = window
        self.current_note_id = None
        
        # Header bar
        self.header = Adw.HeaderBar()
        self.header.set_show_title(False)
        self.header.set_show_start_title_buttons(False)
        
        # Back button for small screens
        back_btn = Gtk.Button(icon_name="go-previous-symbolic")
        back_btn.set_tooltip_text("Not Listesine Dön")
        self.window.inner_split_view.bind_property(
            "collapsed", back_btn, "visible", 
            gi.repository.GObject.BindingFlags.SYNC_CREATE)
        back_btn.connect("clicked", lambda x: self.window.inner_split_view.set_show_sidebar(True))
        self.header.pack_start(back_btn)

        # Title Entry
        self.title_entry = Gtk.Entry()
        self.title_entry.set_placeholder_text("Not Başlığı...")
        self.title_entry.set_hexpand(True)
        self.title_entry.add_css_class("flat")
        self.title_entry.add_css_class("title-1")
        self.title_entry.connect("changed", self.on_content_changed)
        self.header.set_title_widget(self.title_entry)

        # Toolbar buttons
        self.pin_btn = Gtk.ToggleButton(icon_name="view-pin-symbolic")
        self.pin_btn.set_tooltip_text("Sabitle")
        self.pin_btn.connect("toggled", self.on_pin_toggled)
        self.header.pack_end(self.pin_btn)
        
        del_btn = Gtk.Button(icon_name="user-trash-symbolic")
        del_btn.set_tooltip_text("Sil")
        del_btn.connect("clicked", self.on_delete_clicked)
        self.header.pack_end(del_btn)
        
        self.append(self.header)

        # Single editor text view
        self.text_view = Gtk.TextView()
        self.text_view.set_wrap_mode(Gtk.WrapMode.WORD_CHAR)
        self.text_view.set_margin_start(16)
        self.text_view.set_margin_end(16)
        self.text_view.set_margin_top(16)
        self.text_view.set_margin_bottom(16)
        self.text_view.set_editable(True)
        self.text_view.set_can_focus(True)
        self.text_buffer = self.text_view.get_buffer()
        self.text_buffer.connect("changed", self.on_content_changed)
        
        src_scrolled = Gtk.ScrolledWindow()
        src_scrolled.set_child(self.text_view)
        src_scrolled.set_vexpand(True)
        self.append(src_scrolled)
        
        self.save_timeout = 0
        self.updating_ui = False
        
        self.set_sensitive(False)

    def load_note(self, note_id):
        self.updating_ui = True
        self.current_note_id = note_id
        note = self.db.get_note(note_id)
        
        if note:
            self.title_entry.set_text(note['title'] or "")
            self.text_buffer.set_text(note['content'] or "")
            self.pin_btn.set_active(bool(note['is_pinned']))
            self.set_sensitive(True)
            self.text_view.grab_focus()
        else:
            self.clear()
        self.updating_ui = False

    def clear(self):
        self.current_note_id = None
        self.updating_ui = True
        self.title_entry.set_text("")
        self.text_buffer.set_text("")
        self.pin_btn.set_active(False)
        self.set_sensitive(False)
        self.updating_ui = False

    def on_content_changed(self, *args):
        if self.updating_ui or not self.current_note_id:
            return
            
        if self.save_timeout:
            GLib.source_remove(self.save_timeout)
        self.save_timeout = GLib.timeout_add(500, self.do_save)

    def do_save(self):
        self.save_timeout = 0
        if not self.current_note_id:
            return False
            
        title = self.title_entry.get_text()
        start, end = self.text_buffer.get_bounds()
        content = self.text_buffer.get_text(start, end, False)
        
        self.db.update_note(self.current_note_id, title, content)
        self.window.on_note_saved()
        return False

    def on_pin_toggled(self, btn):
        if self.updating_ui or not self.current_note_id:
            return
        self.db.toggle_pin(self.current_note_id)
        self.window.on_note_saved()

    def on_delete_clicked(self, btn):
        if not self.current_note_id:
            return
            
        dialog = Adw.MessageDialog(heading="Notu Sil", body="Bu notu silmek istediğinize emin misiniz?")
        dialog.add_response("cancel", "İptal")
        dialog.add_response("delete", "Sil")
        dialog.set_response_appearance("delete", Adw.ResponseAppearance.DESTRUCTIVE)
        
        def on_response(dialog, response):
            if response == "delete":
                self.db.delete_note(self.current_note_id)
                self.window.on_note_deleted(self.current_note_id)
                
        dialog.connect("response", on_response)
        dialog.set_transient_for(self.window)
        dialog.present()

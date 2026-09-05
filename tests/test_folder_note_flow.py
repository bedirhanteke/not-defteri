import unittest
import tempfile
import os
from app.db import Database

class TestFolderNoteFlow(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.db_path = os.path.join(self.temp_dir.name, "test_flow.db")
        self.db = Database(self.db_path)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_new_note_in_folder_remains_in_folder_after_content_update(self):
        # 1. Create a folder "Ders Notları"
        folder_id = self.db.add_folder("Ders Notları")
        self.assertIsNotNone(folder_id)

        # 2. Create a new note inside "Ders Notları"
        note_id = self.db.add_note("Yeni Not", "", folder_id=folder_id)
        self.assertIsNotNone(note_id)

        # Verify initial note is in "Ders Notları"
        notes_in_folder = self.db.get_notes(folder_id=folder_id)
        self.assertEqual(len(notes_in_folder), 1)
        self.assertEqual(notes_in_folder[0]['id'], note_id)
        self.assertEqual(notes_in_folder[0]['folder_id'], folder_id)

        # 3. Simulate user typing content into editor (auto-save triggers db.update_note)
        self.db.update_note(note_id, "Yeni Not", "Bu klasörün içindeki not içeriği...")

        # 4. Verify note is STILL under "Ders Notları"
        note_after_update = self.db.get_note(note_id)
        self.assertEqual(note_after_update['folder_id'], folder_id)
        self.assertEqual(note_after_update['content'], "Bu klasörün içindeki not içeriği...")

        notes_in_folder_after_update = self.db.get_notes(folder_id=folder_id)
        self.assertEqual(len(notes_in_folder_after_update), 1)
        self.assertEqual(notes_in_folder_after_update[0]['id'], note_id)
        self.assertEqual(notes_in_folder_after_update[0]['folder_id'], folder_id)

    def test_change_note_folder_and_type_content(self):
        # 1. Create Folder A and Folder B
        folder_a_id = self.db.add_folder("Klasör A")
        folder_b_id = self.db.add_folder("Klasör B")

        # 2. Create note in Folder A
        note_id = self.db.add_note("Taşınacak Not", "İçerik A", folder_id=folder_a_id)
        
        # Verify it's in Folder A
        self.assertEqual(len(self.db.get_notes(folder_id=folder_a_id)), 1)
        self.assertEqual(len(self.db.get_notes(folder_id=folder_b_id)), 0)

        # 3. Change note's folder to Folder B (simulating right-click -> Klasör Değiştir -> Klasör B)
        note = self.db.get_note(note_id)
        self.db.update_note(note_id, note['title'], note['content'], folder_id=folder_b_id)

        # Verify note is no longer in Folder A, but in Folder B
        self.assertEqual(len(self.db.get_notes(folder_id=folder_a_id)), 0)
        notes_in_b = self.db.get_notes(folder_id=folder_b_id)
        self.assertEqual(len(notes_in_b), 1)
        self.assertEqual(notes_in_b[0]['id'], note_id)
        self.assertEqual(notes_in_b[0]['folder_id'], folder_b_id)

        # 4. Type new content into note (simulating editor auto-save)
        self.db.update_note(note_id, "Taşınacak Not", "Güncellenmiş İçerik B")

        # 5. Verify note is STILL in Folder B and not reset to NULL / Tüm Notlar
        note_after_edit = self.db.get_note(note_id)
        self.assertEqual(note_after_edit['folder_id'], folder_b_id)
        self.assertEqual(note_after_edit['content'], "Güncellenmiş İçerik B")
        self.assertEqual(len(self.db.get_notes(folder_id=folder_b_id)), 1)

        # 6. Change note's folder to "Klasörsüz (Tüm Notlar)" (folder_id=None)
        self.db.update_note(note_id, note_after_edit['title'], note_after_edit['content'], folder_id=None)
        note_unfoldered = self.db.get_note(note_id)
        self.assertIsNone(note_unfoldered['folder_id'])
        self.assertEqual(len(self.db.get_notes(folder_id=folder_b_id)), 0)

if __name__ == '__main__':
    unittest.main()

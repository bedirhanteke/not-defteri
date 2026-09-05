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

if __name__ == '__main__':
    unittest.main()

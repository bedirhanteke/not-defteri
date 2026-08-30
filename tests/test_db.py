import unittest
import tempfile
import os
from app.db import Database

class TestDatabase(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.db_path = os.path.join(self.temp_dir.name, "test.db")
        self.db = Database(self.db_path)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_add_get_folder(self):
        folder_id = self.db.add_folder("Work")
        self.assertIsNotNone(folder_id)
        
        folders = self.db.get_folders()
        self.assertEqual(len(folders), 1)
        self.assertEqual(folders[0]["name"], "Work")
        
        # Test duplicate folder
        dup_id = self.db.add_folder("Work")
        self.assertIsNone(dup_id)

    def test_rename_folder(self):
        folder_id = self.db.add_folder("Personal")
        res = self.db.rename_folder(folder_id, "Private")
        self.assertTrue(res)
        folders = self.db.get_folders()
        self.assertEqual(folders[0]["name"], "Private")

    def test_delete_folder(self):
        folder_id = self.db.add_folder("Temp")
        note_id = self.db.add_note("N", "C", folder_id)
        self.db.delete_folder(folder_id)
        folders = self.db.get_folders()
        self.assertEqual(len(folders), 0)
        note = self.db.get_note(note_id)
        self.assertIsNone(note["folder_id"])

    def test_add_get_note(self):
        note_id = self.db.add_note("My Note", "Content of note")
        self.assertIsNotNone(note_id)
        
        note = self.db.get_note(note_id)
        self.assertEqual(note["title"], "My Note")
        self.assertEqual(note["content"], "Content of note")
        self.assertFalse(note["is_pinned"])

    def test_update_note(self):
        note_id = self.db.add_note("Title 1", "Content 1")
        self.db.update_note(note_id, "Title 2", "Content 2", folder_id=None)
        
        note = self.db.get_note(note_id)
        self.assertEqual(note["title"], "Title 2")
        self.assertEqual(note["content"], "Content 2")

    def test_delete_note(self):
        note_id = self.db.add_note("T", "C")
        self.db.delete_note(note_id)
        
        note = self.db.get_note(note_id)
        self.assertIsNone(note)

    def test_toggle_pin(self):
        note_id = self.db.add_note("T", "C")
        self.db.toggle_pin(note_id)
        note = self.db.get_note(note_id)
        self.assertTrue(note["is_pinned"])
        
        self.db.toggle_pin(note_id)
        note = self.db.get_note(note_id)
        self.assertFalse(note["is_pinned"])

if __name__ == '__main__':
    unittest.main()

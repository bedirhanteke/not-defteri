import sqlite3
import os
import datetime

_UNSET = object()

class Database:
    def __init__(self, db_path):
        self.db_path = db_path
        self._init_db()

    def get_connection(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _init_db(self):
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        with self.get_connection() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS folders (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT UNIQUE NOT NULL
                )
            """)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS tags (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT UNIQUE NOT NULL
                )
            """)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS notes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    content TEXT NOT NULL,
                    folder_id INTEGER,
                    is_pinned BOOLEAN NOT NULL DEFAULT 0,
                    is_archived BOOLEAN NOT NULL DEFAULT 0,
                    created_at TIMESTAMP NOT NULL,
                    updated_at TIMESTAMP NOT NULL,
                    FOREIGN KEY (folder_id) REFERENCES folders(id)
                )
            """)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS note_tags (
                    note_id INTEGER,
                    tag_id INTEGER,
                    PRIMARY KEY (note_id, tag_id),
                    FOREIGN KEY (note_id) REFERENCES notes(id) ON DELETE CASCADE,
                    FOREIGN KEY (tag_id) REFERENCES tags(id) ON DELETE CASCADE
                )
            """)
            conn.commit()

    def add_folder(self, name):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            try:
                cursor.execute("INSERT INTO folders (name) VALUES (?)", (name,))
                conn.commit()
                return cursor.lastrowid
            except sqlite3.IntegrityError:
                return None

    def get_folders(self):
        with self.get_connection() as conn:
            cursor = conn.execute("SELECT * FROM folders ORDER BY name")
            return [dict(row) for row in cursor.fetchall()]

    def rename_folder(self, folder_id, new_name):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            try:
                cursor.execute("UPDATE folders SET name = ? WHERE id = ?", (new_name, folder_id))
                conn.commit()
                return True
            except sqlite3.IntegrityError:
                return False

    def delete_folder(self, folder_id):
        with self.get_connection() as conn:
            conn.execute("UPDATE notes SET folder_id = NULL WHERE folder_id = ?", (folder_id,))
            conn.execute("DELETE FROM folders WHERE id = ?", (folder_id,))
            conn.commit()

    def add_note(self, title, content, folder_id=None):
        now = datetime.datetime.now().isoformat()
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO notes (title, content, folder_id, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?)
            """, (title, content, folder_id, now, now))
            conn.commit()
            return cursor.lastrowid

    def update_note(self, note_id, title, content, folder_id=_UNSET):
        now = datetime.datetime.now().isoformat()
        with self.get_connection() as conn:
            if folder_id is _UNSET:
                conn.execute("""
                    UPDATE notes SET title = ?, content = ?, updated_at = ?
                    WHERE id = ?
                """, (title, content, now, note_id))
            else:
                conn.execute("""
                    UPDATE notes SET title = ?, content = ?, folder_id = ?, updated_at = ?
                    WHERE id = ?
                """, (title, content, folder_id, now, note_id))
            conn.commit()

    def get_notes(self, folder_id=None, search_query=None, archived=False):
        with self.get_connection() as conn:
            query = "SELECT * FROM notes WHERE is_archived = ?"
            params = [1 if archived else 0]
            
            if folder_id is not None:
                query += " AND folder_id = ?"
                params.append(folder_id)
                
            if search_query:
                query += " AND (title LIKE ? OR content LIKE ?)"
                params.extend([f"%{search_query}%", f"%{search_query}%"])
                
            query += " ORDER BY is_pinned DESC, updated_at DESC"
            
            cursor = conn.execute(query, params)
            return [dict(row) for row in cursor.fetchall()]

    def get_note(self, note_id):
        with self.get_connection() as conn:
            cursor = conn.execute("SELECT * FROM notes WHERE id = ?", (note_id,))
            row = cursor.fetchone()
            return dict(row) if row else None

    def delete_note(self, note_id):
        with self.get_connection() as conn:
            conn.execute("DELETE FROM notes WHERE id = ?", (note_id,))
            conn.commit()

    def toggle_pin(self, note_id):
        with self.get_connection() as conn:
            conn.execute("UPDATE notes SET is_pinned = NOT is_pinned WHERE id = ?", (note_id,))
            conn.commit()
            
    def toggle_archive(self, note_id):
        with self.get_connection() as conn:
            conn.execute("UPDATE notes SET is_archived = NOT is_archived WHERE id = ?", (note_id,))
            conn.commit()

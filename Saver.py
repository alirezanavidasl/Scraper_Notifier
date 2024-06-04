import sqlite3

class Saver:
    def __init__(self, hashlist_file_name, User):
        self.db_path = 'result/hashlist.db'
        self.hashlist_file_name = hashlist_file_name
        self.tableName = User
        self.initialize_db()

    def initialize_db(self):
        # Create a connection to the SQLite database
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            # Create a table for the hashlist file name if it doesn't exist
            cursor.execute(f'''CREATE TABLE IF NOT EXISTS {self.tableName} (
                                hash_file_name TEXT,
                                hash_value TEXT,
                                PRIMARY KEY (hash_file_name, hash_value)
                            )''')

    def hash_exists(self, hash_value):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            # Check if the table for the hashlist file name exists
            cursor.execute('''SELECT name FROM sqlite_master 
                              WHERE type='table' AND name=?''', (self.tableName,))
            if cursor.fetchone() is not None:
                # Table exists, check if the hash exists in the table
                cursor.execute(f'''SELECT hash_value FROM {self.tableName} WHERE hash_file_name = ? AND hash_value = ?''', (self.hashlist_file_name, hash_value))
                return cursor.fetchone() is not None
            else:
                return False

    def append_hash(self, hash_value):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            # Insert the hash into the table
            cursor.execute(f'''INSERT OR IGNORE INTO {self.tableName} (hash_file_name, hash_value) VALUES (?, ?)''', (self.hashlist_file_name, hash_value))

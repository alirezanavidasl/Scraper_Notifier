import sqlite3
from Utils.WriteToFile import WriteToFile as log

class Saver:
    def __init__(self, hashlist_file_name, User):
        self.db_path = 'result/hashlist.db'
        self.hashlist_file_name = hashlist_file_name
        self.tableName = User
        self.initialize_db()

    def initialize_db(self):
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(f'''CREATE TABLE IF NOT EXISTS {self.tableName} (
                                    hash_file_name TEXT,
                                    hash_value TEXT,
                                    PRIMARY KEY (hash_file_name, hash_value)
                                )''')
        except sqlite3.Error as e:
            log.LogErrorToFile(f"SQLite error in initialize_db: {e}")
        except Exception as e:
            log.LogErrorToFile(f"Unexpected error in initialize_db: {e}")

    def hash_exists(self, hash_value):
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''SELECT name FROM sqlite_master 
                                  WHERE type='table' AND name=?''', (self.tableName,))
                if cursor.fetchone() is not None:
                    cursor.execute(f'''SELECT hash_value FROM {self.tableName} WHERE hash_file_name = ? AND hash_value = ?''', (self.hashlist_file_name, hash_value))
                    if cursor.fetchone() is not None:
                        return True
                    else:
                        return False
                else:
                    return False
        except sqlite3.Error as e:
            log.LogErrorToFile(f"SQLite error in hash_exists: {e}")
        except Exception as e:
            log.LogErrorToFile(f"Unexpected error in hash_exists: {e}")
            return False  # Return False in case of an error

    def append_hash(self, hash_value):
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(f'''INSERT OR IGNORE INTO {self.tableName} (hash_file_name, hash_value) VALUES (?, ?)''', (self.hashlist_file_name, hash_value))
        except sqlite3.IntegrityError as e:
            log.LogErrorToFile(f"SQLite integrity error in append_hash: {e}")
        except sqlite3.Error as e:
            log.LogErrorToFile(f"SQLite error in append_hash: {e}")
        except Exception as e:
            log.LogErrorToFile(f"Unexpected error in append_hash: {e}")

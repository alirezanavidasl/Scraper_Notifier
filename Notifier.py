import requests
import sqlite3
from datetime import datetime

class Notifier:

    def __init__(self, token):
        self.bot_token = token
        self.db_path = 'result/hashlist.db'
        self.chat_id = self.get_chat_id_from_db(token,self.db_path)
        if not self.chat_id:
            self.chat_id = self.get_chat_id(token)
            if self.chat_id:
                self.save_chat_id_to_db(token, self.chat_id,self.db_path)

    def send_message(self, message):
        try:
            response = requests.get(f'https://api.telegram.org/bot{self.bot_token}/sendMessage?chat_id={self.chat_id}&text={message}')
            response.raise_for_status()  # Raises an HTTPError if the response status is 4xx, 5xx
        except Exception as e:
            with open('log/error.txt', 'a') as errorFile:
                errorFile.write(f"{datetime.now()} - Failed to send notification: {e}\n")
            print(f"Failed to send notification: {e}")



    @staticmethod
    def get_chat_id(BOT_TOKEN):
        api_url = f'https://api.telegram.org/bot{BOT_TOKEN}/getUpdates'
        try:
            response = requests.get(api_url)
            response.raise_for_status()
            data = response.json()

            if 'result' not in data or not data['result']:
                raise ValueError("Empty or missing 'result' in the response.")
                
            for result in data.get('result', []):
                if 'message' in result and 'chat' in result['message']:
                    chat_id = result['message']['chat']['id']
                    return chat_id
        except Exception as e:
            with open('log/error.txt', 'a') as errorFile:
                errorFile.write(f"{datetime.now()} - Error in get_chat_id: {e}\n")
            print(f"Error in get_chat_id: {e}")
        return None
    
    @staticmethod
    def save_chat_id_to_db(bot_token, chat_id,db_path):
        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS entities (
                    bot_token TEXT,
                    chat_id TEXT
                )
            ''')
            cursor.execute('INSERT INTO entities (bot_token, chat_id) VALUES (?, ?)', (bot_token, chat_id))
            conn.commit()
            conn.close()
        except Exception as e:
            with open('log/error.txt', 'a') as errorFile:
                errorFile.write(f"{datetime.now()} - Failed to save chat_id to database: {e}\n")
            print(f"Failed to save chat_id to database: {e}")
    @staticmethod
    def get_chat_id_from_db(bot_token,db_path):
        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            cursor.execute('SELECT chat_id FROM entities WHERE bot_token = ?', (bot_token,))
            result = cursor.fetchone()
            conn.close()
            if result:
                return result[0]
            return None
        except Exception as e:
            with open('log/error.txt', 'a') as errorFile:
                errorFile.write(f"{datetime.now()} - Failed to retrieve chat_id from database: {e}\n")
            print(f"Failed to retrieve chat_id from database: {e}")
            return None
import requests
import time
from datetime import datetime

class Notifier:

    def __init__(self, token):
        self.bot_token = token
        self.chat_id = self.get_chat_id_with_retry(token)

    def send_message(self, message):
        try:
            response = requests.get(f'https://api.telegram.org/bot{self.bot_token}/sendMessage?chat_id={self.chat_id}&text={message}')
            response.raise_for_status()  # Raises an HTTPError if the response status is 4xx, 5xx
        except Exception as e:
            with open('log/error.txt', 'a') as errorFile:
                errorFile.write(f"{datetime.now()} - Failed to send notification: {e}\n")
            print(f"Failed to send notification: {e}")

    def get_chat_id_with_retry(self, BOT_TOKEN, retries=5, delay=5):
        for attempt in range(retries):
            try:
                chat_id = self.get_chat_id(BOT_TOKEN)
                if chat_id is not None:
                    return chat_id
                else:
                    raise ValueError("Chat ID not found in the response.")
            except Exception as e:
                if attempt < retries - 1:
                    time.sleep(delay)
                else:
                    with open('log/error.txt', 'a') as errorFile:
                        errorFile.write(f"{datetime.now()} - Failed to get chat ID after {retries} attempts: {e}\n")
                    print(f"Failed to get chat ID after {retries} attempts: {e}")
                    return None

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

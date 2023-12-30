import requests

class Notifier:

    def __init__(self, token):

        self.bot_token = token
        self.chat_id = Notifier.get_chat_id(token)

    def send_message(self, message):
        try:
            requests.get(f'https://api.telegram.org/bot{self.bot_token}/sendMessage?chat_id={self.chat_id}&text={message}')
        except Exception as e:
            print(f"Failed to send notification: {e}")

    @staticmethod
    def get_chat_id(BOT_TOKEN):
        api_url = f'https://api.telegram.org/bot{BOT_TOKEN}/getUpdates'
        response = requests.get(api_url)
        data = response.json()
        
        for result in data.get('result', []):
            if 'message' in result and 'chat' in result['message']:
                chat_id = result['message']['chat']['id']
                return chat_id

        return None
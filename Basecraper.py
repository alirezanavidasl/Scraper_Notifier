from abc import ABC, abstractmethod
from Logger import Logger
from Saver import Saver
from Notifier import Notifier
import hashlib

class Basecraper(ABC):
    def __init__(self, classData):

        self.url = classData["URL"]
        self.send_error = True
        self.notifier = Notifier(classData["Bot_token"])
        self.logger=Logger(classData["Name"])
        self.saver = Saver(classData["Bot_token"])

    @abstractmethod
    def scrape(self):
        pass

    def run(self):
        self.scrape()
        self.logger.log_result(True)

    def check_item(self,item_content):

        item_hash = self.make_hash(item_content["specs"])
        if not self.saver.hash_exists(item_hash):

            self.saver.append_hash(item_hash)
            self.notifier.send_message(item_content["specs"])
            self.notifier.send_message(item_content["item_url"])
            self.logger.log_result(True)
            self.send_error = True


    def make_hash(self,specs):
        return hashlib.sha256(str(specs).encode('utf-8')).hexdigest()
    

    def notify_log_error(self,e):

        self.logger.log_result(False, e)
        if self.send_error:
            self.notifier.send_message(f'There is an error: {str(e)}')
            self.send_error = False

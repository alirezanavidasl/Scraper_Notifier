from H2S_Scraper import H2S_Scraper
from Pararius_Scraper import Pararius_Scraper
from Kamernet_Scraper import Kamernet_Scraper
import json
import random,time

with open('../Data.json', 'r') as file:
    data_dict = json.load(file)

scraperInstances = []

for classData in data_dict["Sites_data"]:
        
        scraperObject = getattr(__import__(__name__), f'{classData["Name"]}_Scraper')
        scraperInstance = scraperObject(classData)
        scraperInstances.append(scraperInstance)

while True:
    for scraperInstance in scraperInstances:
        scraperInstance.run()
        scraperInstance.logger.log_cleaner()
    time.sleep(10 + random.randint(1, 4))






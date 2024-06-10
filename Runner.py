from H2S_Scraper import H2S_Scraper
from Pararius_Scraper import Pararius_Scraper
from Kamernet_Scraper import Kamernet_Scraper
from Funda_Scraper import Funda_Scraper

import json, requests
import random,time

# with open('../Data.json', 'r') as file:
#     data_dict = json.load(file)

# with open('../DataTest.json', 'r') as file:
#     data_dict = json.load(file)

file_id_Maryam = "1qIg1daIYEM7KD8GU5DZHPuW-NgHsLED5"
file_id_Test = "1WJblpFpZRLadFX5HM6JtKX2GJ5zeJgRe"

file_ids = [
    {"User":"Maryam","File":file_id_Maryam}
    # {"User":"Test","File":file_id_Test}
    ]

def download_file_from_google_drive(file_id):
    url = f"https://drive.google.com/uc?export=download&id={file_id}"
    response = requests.get(url)
    response.raise_for_status()  # Check if the request was successful
    return response.content

def read_json_from_google_drive(file_id):
    json_content = download_file_from_google_drive(file_id)
    return json.loads(json_content)

def combine_json_from_file_ids(file_ids):
    combined_json = []
    for file_id in file_ids:
        try:
            json_data = read_json_from_google_drive(file_id["File"])
            json_data["User"] = file_id["User"]
            combined_json.append(json_data)
        except requests.exceptions.RequestException as e:
            print(f"Error downloading the file with ID {file_id}: {e}")
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON from file with ID {file_id}: {e}")
    return combined_json

scraperInstances = []


while True:
    
    data_dict_list = combine_json_from_file_ids(file_ids)

    for data_dict in data_dict_list:
        for classData in data_dict["Sites_data"]:
                
                scraperObject = getattr(__import__(__name__), f'{classData["Name"]}_Scraper')
                scraperInstance = scraperObject(classData,data_dict["User"])
                scraperInstances.append(scraperInstance)
    for scraperInstance in scraperInstances:
        scraperInstance.run()
        scraperInstance.logger.log_cleaner()
    time.sleep(10 + random.randint(1, 4))






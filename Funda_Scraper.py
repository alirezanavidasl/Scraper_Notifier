import requests
from bs4 import BeautifulSoup
from Basecraper import Basecraper


class Funda_Scraper(Basecraper):

    

    def scrape(self):

        headers = {
                        'accept': '*/*',
                        'accept-language': 'en-US,en;q=0.9,fa;q=0.8',
                        'origin': 'https://www.funda.nl',
                        'referer': 'https://www.funda.nl/',
                        'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
                        'sec-ch-ua-mobile': '?0',
                        'sec-ch-ua-platform': '"macOS"',
                        'sec-fetch-dest': 'empty',
                        'sec-fetch-mode': 'cors',
                        'sec-fetch-site': 'cross-site',
                        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                    }

        try:
            response = requests.get(self.url,headers=headers)

            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'lxml')
                items = soup.find_all('div', class_='sm:flex')

                for item in items:
                    item_content={}
                    property_info = item.find('div',class_='min-w-0').text

                    # Split the string into lines and remove empty lines
                    lines = [line.strip() for line in property_info.split('\n') if line.strip()]
            
                    # Extracted information
                    address = f"Address: {lines[0]}"
                    postcode = f"PC: {lines[1]}"
                    rent = f"Rent: {lines[2]}"
                    area = f"Area: {lines[3]}"
                    rooms = f"Rooms: {lines[4]}"
                    agent = f"Agent: {lines[5]}"

                    specs = address+'\n'+postcode+'\n'+rent+'\n'+area+'\n'+rooms+'\n'+agent
                    item_content["specs"] = specs
                    item_content["item_url"] = item.find('a').get('href')

                    self.check_item(item_content)

                            

        except Exception as e:
            
            self.notify_log_error(e)

            


import requests
from bs4 import BeautifulSoup
from Basecraper import Basecraper

class Kamernet_Scraper(Basecraper):

    def scrape(self):
        try:
            response = requests.get(self.url)

            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                items = soup.find_all('a', class_='MuiTypography-root MuiTypography-inherit MuiLink-root MuiLink-underlineNone MuiPaper-root MuiPaper-elevation MuiPaper-rounded MuiPaper-elevation1 MuiCard-root ListingCard_root__xVYYt mui-style-y9ap12')

                for item in items:
                    item_content={}

                    item_content["specs"] = item.find('div',class_='MuiCardContent-root ListingCard_cardContent__KkyAH mui-style-1qw96cp').text.strip()
                    item_content["item_url"] = 'https://kamernet.nl/'+item.get('href').lower().replace(" ", "-")

                    self.check_item(item_content)

        except Exception as e:
                        
            self.notify_log_error(e)

            


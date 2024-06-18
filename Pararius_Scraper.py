import requests
from bs4 import BeautifulSoup
from Basecraper import Basecraper


class Pararius_Scraper(Basecraper):

    def scrape(self):
        try:
            response = requests.get(self.url,verify=False)

            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                items = soup.find_all('li', class_='search-list__item search-list__item--listing')

                for item in items:
                    item_content={}
                    title = item.find('div', class_="listing-search-item__sub-title'").text.strip()
                    price = item.find('div', class_="listing-search-item__price").text.strip()
                    desc = item.find('ul', class_="illustrated-features illustrated-features--compact").text.strip()
                    
                    item_content["specs"] = title+'\n'+desc+'\n'+price
                    item_content["item_url"] = 'https://www.pararius.com/'+item.find('a',class_="listing-search-item__link listing-search-item__link--title").get('href')


                    self.check_item(item_content)

                            

        except Exception as e:
            
            self.notify_log_error(e)

            


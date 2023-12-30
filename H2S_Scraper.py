import requests
from bs4 import BeautifulSoup
from Basecraper import Basecraper


class H2S_Scraper(Basecraper):

    def scrape(self):
        try:
            response = requests.get(self.url)

            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                items = soup.find_all('div', class_='regi-item d-flex flex-wrap')

                for item in items:
                    item_content={}
                    is_student=False
                    header_data = item.find('div', class_='item-head').text.strip()
                    header_data = [header_data.split('  ')[0],*header_data.split('  ')[1].split("\n")]
                    for h in header_data:
                        if 'student' in h.lower():
                            is_student=True
                    if not is_student:
                            time_data = item.find('ul', class_='regi-info').text.strip().split('\n')
                            desc = item.find('ul', class_='regi-acm').text.strip().split('\n')
                            price = item.find('div', class_='price regularbold').text.strip().split('\n') 
                            item_content["specs"] = str(header_data)+'\n'+str(time_data)+'\n'+str(desc)+'\n'+str(price)
                            item_content["item_url"] = item.get('data-url')

                            self.check_item(item_content)

                            

        except Exception as e:
            
            self.notify_log_error(e)

            


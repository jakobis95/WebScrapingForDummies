from bs4 import BeautifulSoup
import requests 

html_text = requests.get('https://www.autoscout24.de/lst/?ocs_listing=include&sort=standard&desc=0&bcol=13&ustate=N%2CU&size=20&page=1&cy=D&priceto=15000&kmto=70000&fregto=2018&fregfrom=2016&atype=C&fc=9&qry=&recommended_sorting_based_id=0c74a0df-a318-4ac8-9dea-e21fcdeef8bf&').text
soup = BeautifulSoup(html_text, 'lxml')
car = soup.find('div', class_ = 'cl-list-element cl-list-element-gap')
carname = car.find('h2', class_ = 'cldt-summary-makemodel sc-font-bold sc-ellipsis').text
print(carname)
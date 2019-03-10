import requests
import html5lib
from bs4 import BeautifulSoup
from csv import writer

response = requests.get('http://cargocollective.com/menosketiago')
soup = BeautifulSoup(response.text, 'html5lib')

title = soup.find('title').get_text()

print(title)
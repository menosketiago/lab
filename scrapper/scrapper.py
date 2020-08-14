# This script scrapes my old portfolio site for content and images

import os
import sys
import requests
import html5lib

from bs4 import BeautifulSoup
from csv import writer

response = requests.get('http://cargocollective.com/menosketiago')
soup = BeautifulSoup(response.text, 'html5lib')

path_root = os.path.dirname(sys.modules['__main__'].__file__)
path_thumbs = path_root + 'thumbs/'
path_images = path_root + 'images/'

# Get all the thumbnail wrappers
thumb_wrapper_list = soup.find_all('div', class_='cardimgcrop')
thumb_list = []

# Get the img element from each wrapper and append to thumbs list
for thumb_wrapper in thumb_wrapper_list:
    thumb = thumb_wrapper.find('img')
    thumb_list.append(thumb)

thumb_url_list = []

# Get the highest resolution img url and append it to the thumb_url_list
for thumb in thumb_list:
    if thumb.has_attr('data-4x'):
        thumb_url_list.append(thumb.get('data-4x'))
    elif thumb.has_attr('data-hi-res'):
        thumb_url_list.append(thumb.get('data-hi-res'))
    else:
        thumb_url_list.append(thumb.get('src'))

# Save each img in the url list to the thumbs folder
for url in thumb_url_list:
    # Cleanup the img name
    split_url = url.split('/')
    split_name = split_url[7].replace('_4x', '').split('_')

    if len(split_name) == 3:
        name = split_name[2]
    if len(split_name) == 2:
        name = split_name[1]

    # Save the img with the right name on the destination folder
    with open(path_thumbs + name, 'wb') as file:
        file.write(requests.get(url).content)

from bs4 import BeautifulSoup
from PIL import Image
import requests
import random
import pandas
import time
import json
import sys

def soup_catalog_page(text, id):
    
    soup = BeautifulSoup(text, "lxml")
    dt = [x.get_text().replace(':', '') 
          for x in soup.find_all('dt')]
    dd = [x.get_text().replace('\n', '') 
          for x in soup.find_all('dd')]
    dataDict = dict(zip(dt,dd))

    # We don't care about this value at all.
    _ = dataDict.pop("Rights", None)

    # We checked for existence in scrape_catalog
    with open('data/{} data.txt'.format(id), 'w', encoding = 'utf-8') as file:
        file.write(json.dumps(dataDict))
    return


def scrape_catalog(url, id):
    try:
        with open('data/{} data.txt'.format(id), 'r', encoding = 'utf-8') as file:
            text = file.read()
            return text

    except FileNotFoundError:

        print ("scraping")
        r = requests.get(url)
        time.sleep(2+random.randrange(1,10)*.1)

        if r.status_code != 200:

            print (url)
            print ("Bad HTTP code {}".format(r.status_code))
            return "Add something here"

        soup_catalog_page(r.text, id)
        return

    except Exception as e:

        print(e)
        sys.exit()

def scrape_image(url, id):

    try:
        i = Image.open("data/images/{}.jpg".format(id))
        print ("Loaded from file")
        return

    except FileNotFoundError:

        r = requests.get(url, stream=True)
        r.raw.decode_content=True
        time.sleep(2+random.randrange(1,10)*.1)

        if r.status_code != 200:

            print (url)
            print ("Bad HTTP code {}".format(r.status_code))
            return "Add something here"

        i = Image.open(r.raw)
        i.thumbnail(720)
        i.save("data/images/{}.jpg".format(id))

    except Exception as e:

        print(e)
        sys.exit()

# Set up URLS
page_urls = [(f"https://usdawatercolors.nal.usda.gov/pom/catalog.xhtml"
       f"?id=POM0000{idx:04}") for idx in range(1, 7585)]
image_urls = [(f"https://usdawatercolors.nal.usda.gov/pom/download.xhtml"
        f"?id=POM0000{idx:04}") for idx in range(1, 7585)]

for url in page_urls:
    id = url.split('=')[1]
    print (url)
    scrape_catalog(url, id)

for url in image_urls:
    id = url.split('=')[1]
    print (url)
    scrape_image(url, id)
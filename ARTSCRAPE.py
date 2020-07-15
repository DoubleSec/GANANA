from logzero import logger, logfile
from bs4 import BeautifulSoup
from PIL import Image
import requests
import random
import pandas
import time
import json
import sys

def create_folders():

    for each in ['logs']:
        if not os.path.isdir(each):
            logger.info(f"'{each}' folder does not exist. "
                                f"Making '{each}' folder.")
            os.mkdir('logs')
            logger.info(f"'{each}' folder created.")
    return

def setup_Logfile(logFileName='log'):

    create_folders()
    logfile(f'./logs/{logFileName}.log', backupCount = 2, maxBytes = 1e6)
    logger.info(f"Logfile initiated for {__file__}")

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
    fileName = f"./data/{id} data.txt"
    with open(fileName, 'w', encoding = 'utf-8') as file:
        file.write(json.dumps(dataDict))
    return

def scrape_catalog(url, id):
    
    fileName = f"./data/{id} data.txt"
    try:
        with open(fileName, 'r', encoding = 'utf-8') as file:
            text = file.read()
            return text

    except FileNotFoundError:

        print ("scraping")
        #logger.info(f"Scraping {url}")

        r = requests.get(url)
        time.sleep(2+random.randrange(1,10)*.1)

        if r.status_code != 200:

            print (url)
            print ("Bad HTTP code {}".format(r.status_code))
            #logger.info(f"Scrape failed for {url}"
            #            f"HTTP code {r.status_code}")

            return "Add something here"

        soup_catalog_page(r.text, id)
        return

    except Exception as e:

        print(e)
        #logger.exception(f"{e} for {url}")
        sys.exit()

def scrape_image(url, id):
    
    imageFileName = f'data/images/{id}.jpg'
    try:
        i = Image.open(imageFileName)
        print ("Loaded from file")
        #logger.info(f"Loaded image {id} from file")
        return

    except FileNotFoundError:

        r = requests.get(url, stream=True)
        r.raw.decode_content=True
        time.sleep(2+random.randrange(1,10)*.1)

        if r.status_code != 200:

            print (url)
            print ("Bad HTTP code {}".format(r.status_code))
            #logger.info(f"Scrape failed for {url}"
            #            f"HTTP code {r.status_code}")

            return "Add something here"

        i = Image.open(r.raw)
        # Happens in place
        i.thumbnail((720, 720))
        i.save(imageFileName)
        #logger.info(f"Image {id} saved")

    except Exception as e:

        print(e)
        #logger.exception(f"{e} for {url}")
        sys.exit()

if __name__ == "__main__":
    
    #create_folders()
    #setup_Logfile()
    
    # Set up URLS
    page_urls = [(f"https://usdawatercolors.nal.usda.gov/pom/catalog.xhtml"
          f"?id=POM0000{idx:04}") for idx in range(1, 7585)]
    image_urls = [(f"https://usdawatercolors.nal.usda.gov/pom/download.xhtml"
            f"?id=POM0000{idx:04}") for idx in range(1, 7585)]

    for url in page_urls:
        id = url.split('=')[1]
        print (url)
        #logger.info(f"Next data page to try: {url}")
        scrape_catalog(url, id)

    for url in image_urls:
        id = url.split('=')[1]
        print (url)
        #logger.info(f"Next image page to try: {url}")
        scrape_image(url, id)
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 20 16:51:25 2019
Edited on Tue May 05 

@author: Cédric Berteletti
@edit : Axel Faligot-Girardelli

Adapted for Python 3
Original work: https://gist.github.com/genekogan/ebd77196e4bf0705db51f86431099e57
Also adapted from:
_ http://stackoverflow.com/questions/20716842/python-download-images-from-google-image-search
_ http://penseeartificielle.fr/massive-google-image-scraping/

That program allow the user to download 1 to 100 pictures, up to 5 Mozilla websearch.

/!\ The program need :
    - Mozilla
    - geckodriver.exe in the file
    - selenium package downloaded
    - beautifulsoup package downloaded
    - python 3.8

Usage examples :
_ by command line in Py 3.8: 
py image_search_scraper.py --search "object" --nb_images X --directory "dataset/"
py image_search_scraper.py --search "object1","object2",...,"object5" --nb_images X --directory "dataset/"
_ or directly setting the parameters in the main method and starting the script without command line parameters

usage: image_search_scraper.py [-h] [-s SEARCH] [-n NB_IMAGES] [-f FIRST_INDEX] [-d DIRECTORY]

Be sure to use '"' for terms, and ',' to separate terms.

"""

from collections import Counter
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup
from urllib.request import urlopen, Request
import base64
import os
import argparse
import json
import time


HTTP_TIMEOUT = 10 #seconds


def get_soup(url, header): #fonction get_soup
    with urlopen(Request(url, headers=header), timeout=HTTP_TIMEOUT) as url:
        soup = BeautifulSoup(url, "html.parser")
    return soup

def search_google(header, text_to_search): # no more working since 2020 update
    query = text_to_search.split()
    query = "+".join(query)
    url = "https://www.google.co.in/search?q="+query+"&source=lnms&tbm=isch"
    soup = get_soup(url, header)

    actualImages = [] # contains the link for Large original images, type of image
    for a in soup.find_all("img",{"class":"rg_i"}):
        link, extension = a.attrs["data-iurl"], a.attrs["src"]
        extension = extension.split(";")[0]
        if len(extension) > 0:
            extension = extension.split("/")[1]
        actualImages.append((link, extension))
    
    return actualImages

def search_google_selenium(header, text_to_search):
    # Preparing request
    query = text_to_search.split()
    query = "+".join(query)
    url = "https://www.google.co.in/search?q="+query+"&source=lnms&tbm=isch"

    # Loading the page with Firefox (via Selenium)
    options = Options()
    options.headless = True
    driver = webdriver.Firefox(options=options)
    driver.get(url)
    headers = {}
    headers['User-Agent'] = "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36"
    extensions = {"jpg", "jpeg", "png", "gif"}

    # Multiple scrolls needed to show all 400 images
    for __ in range(10):        
        driver.execute_script("window.scrollBy(0, 1000000)")
        time.sleep(0.2)

    # Searching in the page for image tags
    actualImages = []
    images = driver.find_elements_by_xpath('//img[contains(@class,"rg_i")]')

    # Getting image data
    for image in images:
        link = image.get_attribute("src")
        if link is not None:
            if link.startswith("data:image/jpeg;base64,"):
                link = link[len("data:image/jpeg;base64,"):]
                extension = "data:image/jpeg;base64"            
            else:
                extension = "jpg"
            actualImages.append((link, extension))
    
    driver.quit()
    return actualImages

def search_bing(header, text_to_search): # not working
    query = text_to_search.split()
    query = "+".join(query)
    url = "https://www.bing.com/images/search?q="+query
    soup = get_soup(url, header)

    actualImages = [] # contains the link for Large original images, type of image
    for a in soup.find_all("a",{"class":"iusc"}):
        #meta = a.attrs["m"].split(",")
        meta = json.loads(a.attrs["m"])
        link = meta["murl"].split("?")[0]
        extensionIndex = link.rfind(".") + 1
        if extensionIndex > -1:
            extension = link[extensionIndex:]
        else:
            extension = ""
        actualImages.append((link, extension))
    
    return actualImages

def search_qwant(header, text_to_search): # not working
    query = text_to_search.split()
    query = "%20".join(query)
    url = "https://www.qwant.com/?q=" + query + "&t=images"
    soup = get_soup(url, header)

    actualImages = [] # contains the link for Large original images, type of image
    for a in soup.find_all("div",{"class":"result result--images"}):
        #meta = a.attrs["m"].split(",")
        meta = json.loads(a.attrs["m"])
        link = meta["murl"].split("?")[0]
        extensionIndex = link.rfind(".") + 1
        if extensionIndex > -1:
            extension = link[extensionIndex:]
        else:
            extension = ""
        actualImages.append((link, extension))
    
    return actualImages

def search_duck(header, text_to_search): # not working
    query = text_to_search.split()
    query = "+".join(query)
    url = "https://duckduckgo.com/?q=" + query + "&t=hr&iar=images&iax=images&ia=images"
    soup = get_soup(url, header)

    actualImages = [] # contains the link for Large original images, type of image
    for a in soup.find_all("div",{"class":"tile-wrap"}):
        #meta = a.attrs["m"].split(",")
        meta = json.loads(a.attrs["m"])
        link = meta["murl"].split("?")[0]
        extensionIndex = link.rfind(".") + 1
        if extensionIndex > -1:
            extension = link[extensionIndex:]
        else:
            extension = ""
        actualImages.append((link, extension))
    
    return actualImages


def search_and_save(text_to_search, number_of_images, first_position, root_path):    
    header = {"User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36"}

    # Creating a folder for the images
    path = root_path + text_to_search.replace(" ", "_")
    if not os.path.exists(path):
        os.makedirs(path)

    # Selecting a search engin
    #actualImages = search_google(header, text_to_search)
    actualImages = search_google_selenium(header, text_to_search)
    #actualImages = search_bing(header, text_to_search)
    #actualImages = search_qwant(header, text_to_search)
    #actualImages = search_duck(header, text_to_search)

    # Writing image files from the results
    for i, (img, extension) in enumerate(actualImages[first_position:first_position+number_of_images]):
        try:
            if extension == "data:image/jpeg;base64":
                # Image raw data already in the result
                print("Converting image N°", i)
                raw_img = base64.b64decode (img)
                extension = "jpg"
            else:
                # The result is an url of an image to be downloaded
                req = Request(img, headers=header)
                print("Opening image N°", i, ": ", img)
                with urlopen(req, timeout=HTTP_TIMEOUT) as urlimage:
                    raw_img = urlimage.read()
                    print("Image read")

            # Writing the image file on disk
            if len(extension) == 0:
                f = open(os.path.join(path , "img" + "_" + str(i) + ".jpg"), "wb")
            else:
                f = open(os.path.join(path , "img" + "_" + str(i) + "." + extension), "wb")
            f.write(raw_img)
            f.close()
        except Exception as e:
            print("could not load : ", img)
            print(e)
def main(args):
    if(len(args) > 1):
        # parse the command line parameters if any
        parser = argparse.ArgumentParser(description="Scrap Google images")
        parser.add_argument("-s", "--search", default="gazelle", type=str, help="Search term")
        parser.add_argument("-n", "--nb_images", default=10, type=int, help="Nb images to save")
        parser.add_argument("-f", "--first_index", default=0, type=int, help="First image to save")
        parser.add_argument("-d", "--directory", default="data/", type=str, help="Save directory")
        args = parser.parse_args()  
        
        #query = [args.search]
        ################################################
        query = queryInit = [args.search]
        chain = coc = queryInit[0]
        sep = ',' 
        esp = coc.count(sep)
        listR=[]
        
        if esp > 4:
            print("You are not allowed to websearch more than 5 terms.")
        else :
            startR = 0
            total = 0
            if coc.count(sep)!=0:
                endR = coc.index(sep)
            else:
                endR = len(coc)  
            pos=endR  
            print(pos)
            for i in range(0,esp):
                if i ==0 : total = total + pos
                elif i==1 : total = total + pos + i
                elif i==2 : total = total + pos + i
                elif i==3 : total = total + pos + i+(2-i)
                
                listR.append(total)
                coc = coc[endR+1:]
                if coc.count(sep)!=0:
                    endR = coc.index(sep)+1
                    pos = coc.index(sep)
                else : break 
                
        print(listR)                            
        
        init = 0
        query=[]
        
        for z in range(len(listR)-1):
            query.append(chain[init:listR(z)]) 
            init = init + listR(z)+1  
        
        if args.nb_images > 100 :
            print("You are not allowed to download more than 100 pictures by websearch.")
        else :
            max_images = args.nb_images
        ##############################################################     
        
        #query = [args.search]
        #max_images = args.nb_images
        first_image_index = args.first_index
        save_directory = args.directory
    else:
        # if no command line parameter, directly use these parameters:
        query = ["gazelle thomson", "gazelle grant", "monkey", "giraffe",
                   "lion", "leopard", "elephant", "rhinoceros", "hyppopotame"]
        max_images = 100
        first_image_index = 0
        save_directory = "dataset/"

    for text in query:
        search_and_save(text, max_images, first_image_index, save_directory)


if __name__ == "__main__":
    from sys import argv
    try:
        main(argv)
    except KeyboardInterrupt:
        pass


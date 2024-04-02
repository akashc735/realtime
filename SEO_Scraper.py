import requests
from bs4 import BeautifulSoup
import urllib
import json


def parse_data(allData):
    g = 0
    Data = []
    l = {}
    for i in range(0, len(allData)):
        link = allData[i].find('a').get('href')

        if (link is not None):
            if (link.find('https') != -1 and link.find('http') == 0 and link.find('aclk') == -1):
                g = g+1
                l["link"] = link
                try:
                    l["title"] = allData[i].find('h3').text
                except:
                    l["title"] = None

                Data.append(l)

                l = {}

            else:
                continue

        else:
            continue
    return Data


def display_results(json_data):
    print(json.dumps(json_data, indent=2))


def extract_info(URL):
    seo_info = {}
    html = requests.get(URL)
    soup = BeautifulSoup(html.text, 'html.parser')

    seo_info["link"] = URL
    try:
        seo_info["metatitle"] = (soup.find('title')).get_text()
    except:
        seo_info["metatitle"] = None
    try:
        seo_info["metadescription"] = soup.find(
            'meta', attrs={'name': 'description'})["content"]
    except:
        seo_info["metadescription"] = None
    try:
        seo_info["robots directives"] = soup.find('meta', attrs={'name': 'robots'})[
            "content"].split(",")
    except:
        seo_info["robots directives"] = None
    try:
        seo_info["viewport"] = soup.find(
            'meta', attrs={'name': 'viewport'})["content"]
    except:
        seo_info["viewport"] = None
    try:
        seo_info["charset"] = soup.find(
            'meta', attrs={'charset': True})["charset"]
    except:
        seo_info["charset"] = None
    try:
        seo_info["html language"] = soup.find('html')["lang"]
    except:
        seo_info["html language"] = None

    try:
        seo_info["canonical"] = soup.find(
            'link', attrs={'rel': 'canonical'})["href"]
    except:
        seo_info["canonical"] = None
    try:
        seo_info["list hreflangs"] = [[a['href'], a["hreflang"]]
                                      for a in soup.find_all('link', href=True, hreflang=True)]
    except:
        seo_info["list hreflangs"] = None
    try:
        seo_info["mobile alternate"] = soup.find(
            'link', attrs={'media': 'only screen and (max-width: 640px)'})["href"]
    except:
        seo_info["mobile alternate"] = None

    return seo_info

def search_google(search_query):
    query = urllib.parse.quote_plus(search_query)

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'}
    url = 'https://www.google.com/search?q={query}'.format(query=query)
    html = requests.get(url, headers=headers)

    soup = BeautifulSoup(html.text, 'html.parser')

    allData = soup.find_all("div", {"class": "g"})

    results = parse_data(allData)

    seo_info_hold = []
    err_links = []
    for i in results:
        try:
            value = extract_info(i["link"])
            seo_info_hold.append(value)
        except:
            err_links.append(i["link"])

    print("Scraped SEO results : \n")
    display_results(seo_info_hold)

    if (len(err_links) > 0):
        print("\nCan't able to scrape these links : \n")
        # display_results(err_links)
    return seo_info_hold;

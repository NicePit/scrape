import requests
from bs4 import BeautifulSoup
import re


class ExtractProfile(object):

    def __init__(self, npage):
        self.url = "http://www.chictopia.com/browse/people/" + str(npage) + "?g=1"
        self.links = self.get_item_url()

    def get_item_url(self):
        links_list = []
        html_page = requests.get(self.url)
        soup = BeautifulSoup(html_page.content)
        data = soup.find_all("div", {"class": "bold px12 white lh12 ellipsis"})
        for item in data:
            links_list.append("http://www.chictopia.com" + str(item).split('"')[3])
        return links_list


class ExtractData(object):

    def __init__(self, page_url):
        html_page = requests.get(page_url)
        self.soup = BeautifulSoup(html_page.content)
        self.picture = self.get_pic()
        self.tags = self.get_tags()
        self.keywords = self.get_keywords()
        self.wrap = self.wrapup()

    def get_pic(self):

        image = self.soup.find_all("img", {"itemprop": "image"})
        picture = str(image[0]).split('"')[11]
        return picture

    def get_tags(self):

        tag_list = []
        tags = self.soup.find_all("div", {"class": "left clear px10"})
        for item in tags:
            string = str(item)
            n = re.compile('>(.*?)<', re.DOTALL).findall(string)
            for thing in n:
                if len(thing) > 2:
                    tag_list.append(thing)
        return tag_list

    def get_keywords(self):

        keywords_list = []
        keywords = self.soup.find_all("div", {"class": "garmentLinks left"})

        for item in keywords:
            string = str(item)
            m = re.compile('>(.*?)<', re.DOTALL).findall(string)
            for thing in m:
                if len(thing) > 2:
                    keywords_list.append(thing)
        return keywords_list

    def wrapup(self):
        dicty = {}
        dicty['url'] = self.picture
        dicty['tags'] = self.tags
        dicty['keywords'] = self.keywords
        return dicty



dictionary = {}

for number in range(1,1000):
    roster = ExtractProfile(number)
    for link in roster.links:
        page = ExtractData(link)
        dictionary[number*roster.links.index(link)] = page.wrap

    print "Pages scraped:", len(dictionary)



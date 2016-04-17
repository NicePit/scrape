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

    def get_pic(self):

        image = self.soup.find_all("img", {"itemprop": "image"})
        picture = str(image[0]).split('"')[11]
        return picture

    def get_tags(self):

        tag_dic = []
        tags = self.soup.find_all("div", {"class": "left clear px10"})
        for item in tags:
            string = str(item)
            m = re.compile('>(.*?)<', re.DOTALL).findall(string)
            for thing in m:
                if len(thing) > 2:
                    tag_dic.append(item)
        return tag_dic

    def get_keywords(self):

        keywords_dic = []
        keywords = self.soup.find_all("div", {"class": "garmentLinks left"})

        for item in keywords:
            string = str(item)
            m = re.compile('>(.*?)<', re.DOTALL).findall(string)
            for thing in m:
                if len(thing) > 2:
                    keywords_dic.append(thing)
        return keywords_dic


    def wrapping(self):
        pass


count = 0

for number in range(1,1000):
    roster = ExtractProfile(number)
    for link in roster.links:
        page = ExtractData(link)
        print page.picture
        print page.tags
        print page.keywords

    count += 1
    print count


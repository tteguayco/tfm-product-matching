from collections import deque
import urllib.request
import re
import NodeURL

DEFAULT_STARTING_URL = "https://www.digicamdb.com/cameras/"
DEFAULT_HEADER_URL = "https://www.digicamdb.com/"

REGEX_URL_LEVEL_0 = "<div class=\"brd_inner_div\">\s{0,20}?<a href=\"([^\"]{1,500}?\")\""
REGEX_URL_DETAIL_LEVEL_1 = ""
REGEX_URL_NEXTPAGE_LEVEL_1 = ""

class URLCollector():

    def __init__(self,
                 starting_url=DEFAULT_STARTING_URL, 
                 header_url=DEFAULT_HEADER_URL):
        self.starting_url = starting_url
        self.header_url = header_url
        self.queue = deque()

    def get_html(self, url):
        f = urllib.request.urlopen(url)
        html = f.read()
        return html.decode("utf-8") 

    def add_header_to_url(self, url):
        
        if self.header_url not in url:
            return self.header_url + url
        else:
            return url

    def navigate_level(self, url, level):
        html = self.get_html(url)
        nodesURL = []

        if level == 0:
            m = re.search(REGEX_URL_LEVEL_0, html, re.MULTILINE)
            if m:
                for i in range(0, len(m.groups)):
                    new_url = m.groups(i)
                    new_level = level + 1
                    nodeURL = NodeURL(new_url, new_level)
                    self.queue.append(nodeURL)
            else:
                print("No match")

    def start(self):
        self.navigate_level(self.starting_url, 0)

        while len(self.queue) > 0:
            nodeURL = self.queue.popleft()
            url = nodeURL.url
            level = nodeURL.level

            self.navigate_level(url, level)

            print(self.queue)
            exit()

    def dump2csv(self, output_filepath):
        pass

urlCollector = URLCollector(DEFAULT_STARTING_URL, DEFAULT_HEADER_URL)
urlCollector.start()

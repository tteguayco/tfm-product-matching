from collections import deque
import time
import re
import NodeURL
import common

DEFAULT_STARTING_URL = "https://www.digicamdb.com/cameras/"
DEFAULT_HEADER_URL = "https://www.digicamdb.com/"

REGEX_URL_LEVEL_0 = "<div class=\"brd_inner_div\">\s{0,20}?<a href=\"([^\"]{1,500}?)\""
REGEX_URL_NEXTPAGE_LEVEL_1 = "<a href=\"([^\"]{1,500}?)\">\s{0,4}?Next\s{0,4}?.{1,10}?</a>"
REGEX_URL_DETAIL_LEVEL_1 = "<a class=\"newest\" href=\"([^\"]{1,500}?)\""

OUTPUT_FILEPATH = "../_data/DigitalCameraDetailPageURLs.txt"

class URLCollector():

    def __init__(self,
                 starting_url=DEFAULT_STARTING_URL,
                 header_url=DEFAULT_HEADER_URL):
        self.starting_url = starting_url
        self.header_url = header_url
        self.queue = deque()
        self.urls2detail = []

    def navigate_level(self, url, level):
        html = common.get_html(url)
        m2subnavigation = None
        m2detail = None

        if level == 0:
            m2subnavigation = re.findall(REGEX_URL_LEVEL_0, html, re.MULTILINE)
        else:
            m2subnavigation = re.findall(REGEX_URL_NEXTPAGE_LEVEL_1, html, re.MULTILINE)
            m2detail = re.findall(REGEX_URL_DETAIL_LEVEL_1, html, re.MULTILINE)

        if m2subnavigation:
            for i in range(0, len(m2subnavigation)):
                new_url = common.add_header_to_url(self.header_url, m2subnavigation[i])
                new_level = 1
                nodeURL = NodeURL.NodeURL(new_url, new_level)
                print("Generated URL in level {{{}}}: {}".format(level, new_url))

                # Add nodeURL to queue to process later
                self.queue.append(nodeURL)

        if m2detail:
            for i in range(0, len(m2detail)):
                new_url = common.add_header_to_url(self.header_url, m2detail[i])
                new_level = level + 1
                nodeURL = NodeURL.NodeURL(new_url, new_level)
                print("Generated URL to detail page in level {{{}}}: {}".format(level, new_url))

                # Add nodeURL to list of URLs pointing to product detail pages
                self.urls2detail.append(nodeURL)

    def start(self):
        self.navigate_level(self.starting_url, 0)

        while len(self.queue) > 0:
            nodeURL = self.queue.popleft()
            url = nodeURL.url
            level = nodeURL.level

            self.navigate_level(url, level)

    def dump_detail_urls(self, output_filepath):

        with open(output_filepath, 'w+') as f:
            for nodeURL in self.urls2detail:
                f.write(nodeURL.url + "\n")


if __name__ == "__main__":
    urlCollector = URLCollector(DEFAULT_STARTING_URL, DEFAULT_HEADER_URL)
    
    start_time = time.time()
    urlCollector.start()
    finish_time = time.time()

    urlCollector.dump_detail_urls(OUTPUT_FILEPATH)

    print("URLs to product detail pages generated. Process took {} seconds"
        .format(round(finish_time - start_time, 3)))

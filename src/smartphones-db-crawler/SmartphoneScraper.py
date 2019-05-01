from collections import deque
import time
import re
import NodeURL
import utils
import Product

DEFAULT_STARTING_URL = "https://www.gsmarena.com/"
DEFAULT_HEADER_URL = "https://www.gsmarena.com/"

CUT_LEVEL_0 = "class=\"brandmenu-v2 (.{1,10000}?)</ul>\s{0,4}?<p class=\"pad\""
REGEX_URL_LEVEL_0 = "<li><a\s{0,4}?href=\"([^\"]{1,500}?)\"[^>]{0,500}?>[^<]{1,300}?</a>"
REGEX_URL_NEXTPAGE_LEVEL_1 = "<a class=\"pages-next\" href=\"([^\"]{1,500}?)\""
REGEX_URL_DETAIL_LEVEL_1 = "<a class=\"newest\" href=\"([^\"]{1,500}?)\""

REGEX_BRAND = "class=\"article-info-name\">(.{1,50}?)\sphones<"
REGEX_MODEL = "<strong>\s{0,4}?<span>([^<]{1,100}?)</span>\s{0,4}?</strong>"

OUTPUT_FILEPATH = "../_data/SmartphonesBrandsModels.csv"


class URLCollector():

    def __init__(self,
                 starting_url=DEFAULT_STARTING_URL,
                 header_url=DEFAULT_HEADER_URL):
        self.starting_url = starting_url
        self.header_url = header_url

        self.queue = deque()
        self.products = []

    def get_products_from_list(self, html_list, source_url):
        products = []
        brand = ""

        print("Getting products info from: {}".format(source_url))

        m2brand = re.findall(REGEX_BRAND, html_list, re.MULTILINE)
        m2model = re.findall(REGEX_MODEL, html_list, re.MULTILINE)

        if m2brand:
            brand = m2brand[0]

        if m2model:
            for i in range(len(m2model)):
                product = Product.Product()
                product.brand = brand
                product.model = m2model[i]
                product.url = source_url

                products.append(product)

        return products

    def navigate_level(self, url, level):
        html = utils.get_html(url)
        m2nextpage = None
        m2detail = None

        if level == 0:
            m2html_cut = re.findall(CUT_LEVEL_0, html, re.MULTILINE)
            cut = m2html_cut[0]
            m2nextpage = re.findall(REGEX_URL_LEVEL_0, cut, re.MULTILINE)
        else:
            m2nextpage = re.findall(REGEX_URL_NEXTPAGE_LEVEL_1, html, re.MULTILINE)

            # Stored crawled product's info
            products = self.get_products_from_list(html, url)
            for p in products:
                self.products.append(p)    
            
        if m2nextpage:
            for i in range(0, len(m2nextpage)):
                new_url = utils.add_header_to_url(self.header_url, m2nextpage[i])
                new_level = 1
                nodeURL = NodeURL.NodeURL(new_url, new_level)
                print("Generated URL in level {{{}}}: {}".format(level, new_url))

                # Add nodeURL to queue to process later
                self.queue.append(nodeURL)

    def start(self):
        self.navigate_level(self.starting_url, 0)

        while len(self.queue) > 0:
            nodeURL = self.queue.popleft()
            url = nodeURL.url
            level = nodeURL.level

            self.navigate_level(url, level)

    def dump_detail_urls(self, output_filepath):

        with open(output_filepath, 'w+') as f:
            for p in self.products:
                f.write(p.brand + ",")    
                f.write(p.model + ",")
                f.write(p.url + "\n")


if __name__ == "__main__":
    urlCollector = URLCollector(DEFAULT_STARTING_URL, DEFAULT_HEADER_URL)
    
    start_time = time.time()
    urlCollector.start()
    finish_time = time.time()

    urlCollector.dump_detail_urls(OUTPUT_FILEPATH)

    print("Products info crawled. Process took {} seconds"
        .format(round(finish_time - start_time, 3)))

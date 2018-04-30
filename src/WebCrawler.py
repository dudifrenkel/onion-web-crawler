import arrow
import requests
import time
from tinydb import TinyDB, Query
from lxml import html
import schedule
import StrongholdParser as StParser

# Initialize constants:
URL_DB_NAME = "StrongholdPasteURLs.json"
DB_NAME = "StrongholdPaste.json"
NEW_PASTES = "{} Added {} new pastes"

# Name constants:
TITLE = "title"
AUTHOR = "author"
DATE = "date"
CONTENT = "content"
UNKNOWN_CONS = "Unknown"
GUEST_CONS = "Guest"
ANONYMOUS_AUTHOR = "Anonymous"
URL = "url"
HREF = "href"


class WebCrawler:
    """ This class represent a pastes web crawler """
    def __init__(self):
        self.db = TinyDB(DB_NAME)
        self.urls_db = TinyDB(URL_DB_NAME)
        self.session = WebCrawler.connect_tor()

    def looks_new_pastes(self):
        """ Parsing the page according to given urls and insert parsing
            content to the data base """
        print("looks_new_pastes: ")
        counter = 0
        for i in range(1, 9):
            main_page_tree = self.get_page_tree(StParser.MAIN_PAGE + str(i))
            pastes_urls = StParser.get_page_urls(main_page_tree)
            for url in pastes_urls:
                if not self.get_data_to_db(url):
                    print(NEW_PASTES.format(arrow.utcnow().format(), counter))
                    return
                counter += 1

    def get_data_to_db(self, url):
        """ The method gets a url, parses it, gets his data in json format and
            insert it to the appropriate dbs return true in case of success
            otherwise, false """

        # Checks also the new url not already seen before
        if url and not self.urls_db.contains(Query()[URL] == url):
            response = self.session.get(url)
            tree = html.fromstring(response.content)

            title, content, author, date = StParser.parse_paste(tree)
            self.db.insert({TITLE: title, AUTHOR: author, DATE: str(date),
                            CONTENT: content})
            self.urls_db.insert({URL: url})
            return True
        else:
            return False

    def insert_first_page(self, pastes_urls):
        """ Parsing the page according to given urls and insert parsing
            content to the data base """
        counter = 0
        for url in pastes_urls:
            if not self.get_data_to_db(url):
                print(NEW_PASTES.format(arrow.utcnow().format(), counter))
                return
            counter += 1
        print(NEW_PASTES.format(arrow.utcnow().format(), counter))

    def get_page_tree(self, main_page):
        """ The method gets a main page url and return the tree element
            of this page """
        response = self.session.get(main_page)
        return html.fromstring(response.content)

    @staticmethod
    def connect_tor():
        """ Establish session and define proxies using requests and
            return a session """
        session = requests.session()
        session.proxies = {'http': 'socks5h://localhost:9050',
                           'https': 'socks5h://localhost:9050'}
        return session

    @staticmethod
    def main():
        wc = WebCrawler()

        main_page_tree = wc.get_page_tree(StParser.MAIN_PAGE + str(1))
        pastes_urls = StParser.get_page_urls(main_page_tree)
        wc.insert_first_page(pastes_urls)

        # Schedule the 'look new paste' function to run every 4 hours
        schedule.every(4).hours.do(WebCrawler.looks_new_pastes)

        while 1:
            schedule.run_pending()
            time.sleep(1)


if __name__ == "__main__":
    print("---Start crawling---")
    WebCrawler.main()
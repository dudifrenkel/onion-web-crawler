import WebCrawler as WebCr
import arrow

# X PATH and format constants:
URLS_XPATH = '//a[@class="btn btn-success"]'
CONTENT_XPATH = '//div[@class="text"]/ol/li/div[@style]'
AUTH_DATE_XPATH_REG = '//div[@class="col-sm-6"]/a'
AUTH_DATE_XPATH_NOT_REG = '//div[@class="col-sm-6"]'
TITLE_XPATH = '//div[@class="col-sm-5"]/h4'

AUTH_DAT_PRE = "Posted by "
AUTH_DATE_DELI = " at "
CURRENT_WEB_TIME_FORMAT = "D MMM YYYY, HH:mm:ss UTC"

MAIN_PAGE = "http://nzxj65x32vh2fkhk.onion/all?page="

AUTHOR_IND = 0
DATE_IND = 1


def parse_paste(tree):
    """ The function parsing the given paste according to given tree element
        returns four strings: title, content, author, date """
    # title
    title = (tree.xpath(TITLE_XPATH))[0].text

    # content
    con_lines = tree.xpath(CONTENT_XPATH)
    content = ""
    for line in con_lines:
        if line.text.strip():
            content += line.text.strip() + '\n'

    # author and date
    details = tree.xpath(AUTH_DATE_XPATH_REG)
    if details:     # The author is registered on the website
        author = details[0].text
        date = details[0].tail
    else:
        details = tree.xpath(AUTH_DATE_XPATH_NOT_REG)
        details_text = details[0].text.strip().replace(AUTH_DAT_PRE, "")
        author_date = details_text.split(AUTH_DATE_DELI)
        author = author_date[AUTHOR_IND]
        date = author_date[DATE_IND]

    title, author, date = normalize(title, author, date)

    return title, content, author, date


def normalize(title, author_name, date):
    """ The function normalize title, author and date according to the given
     instructions """
    date = arrow.get(date, CURRENT_WEB_TIME_FORMAT)  # Get UTC format by arrow

    if author_name == WebCr.GUEST_CONS:  # Set all the options to "Anonymous"
        author_name = WebCr.ANONYMOUS_AUTHOR
    elif author_name == WebCr.UNKNOWN_CONS:
        author_name = WebCr.ANONYMOUS_AUTHOR

    title = title.strip()
    return title, author_name, date


def get_page_urls(tree):
    """ The function gets a tree element of a web page and returns list with
     all the pastes' URLs """
    urls_list = []
    pastes_urls = tree.xpath(URLS_XPATH)
    for item in pastes_urls:
        urls_list.append(item.attrib.get(WebCr.HREF))
    return urls_list

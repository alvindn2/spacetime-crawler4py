import re
from urllib.parse import urlparse, urldefrag
from urllib.request import urlopen
import html.parser
from bs4 import BeautifulSoup
import utils


unique_pages = set()


def scraper(url: str, resp: utils.response.Response):
    defrag_url = urldefrag(url)[0]
    links = extract_next_links(defrag_url, resp)
    return [link for link in links if is_valid(link)]


def extract_next_links(url, resp):
    # Implementation requred.
    if is_valid(url):
        f = urlopen(url)
        html_object = BeautifulSoup(f, "html.parser")
        links = [link.get('href') for link in html_object.find_all('a')]
        return links


def is_valid(url):
    try:
        parsed = urlparse(url)
        url_path = parsed.hostname + parsed.path

        valid_hostname = any(host in url for host in (".ics.uci.edu/",
                                            ".cs.uci.edu/",
                                            ".informatics.uci.edu/",
                                            ".informatics.uci.edu/",
                                            ".stat.uci.edu/",
                                            "today.uci.edu/department/information_computer_sciences/"))

        valid_scheme = parsed.scheme in set(["http", "https"])

        no_extension = not re.match(
            r".*\.(css|js|bmp|gif|jpe?g|ico"
            + r"|png|tiff?|mid|mp2|mp3|mp4"
            + r"|wav|avi|mov|mpeg|ram|m4v|mkv|ogg|ogv|pdf"
            + r"|ps|eps|tex|ppt|pptx|doc|docx|xls|xlsx|names"
            + r"|data|dat|exe|bz2|tar|msi|bin|7z|psd|dmg|iso"
            + r"|epub|dll|cnf|tgz|sha1"
            + r"|thmx|mso|arff|rtf|jar|csv"
            + r"|rm|smil|wmv|swf|wma|zip|rar|gz)$", parsed.path.lower())

        is_valid_url = valid_hostname and valid_scheme and no_extension

        if is_valid_url:
            unique_pages.add(url_path)
            return True
        else:
            return False

    except TypeError:
        print ("TypeError for ", parsed)
        raise
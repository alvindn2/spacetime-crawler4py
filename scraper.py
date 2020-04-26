from urllib.parse import urlparse, urldefrag
from urllib.request import urlopen
from bs4 import BeautifulSoup
from collections import Counter, defaultdict
import html.parser
import utils
import re
import tldextract


unique_pages = set()


def scraper(url: str, resp):
    links = extract_next_links(url, resp)
    return [link for link in links if is_valid(link)]


def extract_next_links(url, resp):
    # Implementation requred.
    if is_valid(url) and resp.status in range(200, 300):
        html_object = BeautifulSoup(resp.raw_response.content, "html.parser")
        links = [link.get('href') for link in html_object.find_all('a')]
        return links


def is_valid(url):
    try:
        defrag_url = urldefrag(url)[0]
        parsed = urlparse(defrag_url)
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
            return True
        else:
            return False

    except TypeError:
        print("TypeError for ", parsed)
        raise

# store the stopwords
stopwords = ['a', 'about', 'above', 'across', 'after', 'afterwards']
stopwords += ['again', 'against', 'all', 'almost', 'alone', 'along']
stopwords += ['already', 'also', 'although', 'always', 'am', 'among']
stopwords += ['amongst', 'amoungst', 'amount', 'an', 'and', 'another']
stopwords += ['any', 'anyhow', 'anyone', 'anything', 'anyway', 'anywhere']
stopwords += ['are', 'around', 'as', 'at', 'back', 'be', 'became']
stopwords += ['because', 'become', 'becomes', 'becoming', 'been']
stopwords += ['before', 'beforehand', 'behind', 'being', 'below']
stopwords += ['beside', 'besides', 'between', 'beyond', 'bill', 'both']
stopwords += ['bottom', 'but', 'by', 'call', 'can', 'cannot', 'cant']
stopwords += ['co', 'computer', 'con', 'could', 'couldnt', 'cry', 'de']
stopwords += ['describe', 'detail', 'did', 'do', 'done', 'down', 'due']
stopwords += ['during', 'each', 'eg', 'eight', 'either', 'eleven', 'else']
stopwords += ['elsewhere', 'empty', 'enough', 'etc', 'even', 'ever']
stopwords += ['every', 'everyone', 'everything', 'everywhere', 'except']
stopwords += ['few', 'fifteen', 'fifty', 'fill', 'find', 'fire', 'first']
stopwords += ['five', 'for', 'former', 'formerly', 'forty', 'found']
stopwords += ['four', 'from', 'front', 'full', 'further', 'get', 'give']
stopwords += ['go', 'had', 'has', 'hasnt', 'have', 'he', 'hence', 'her']
stopwords += ['here', 'hereafter', 'hereby', 'herein', 'hereupon', 'hers']
stopwords += ['herself', 'him', 'himself', 'his', 'how', 'however']
stopwords += ['hundred', 'i', 'ie', 'if', 'in', 'inc', 'indeed']
stopwords += ['interest', 'into', 'is', 'it', 'its', 'itself', 'keep']
stopwords += ['last', 'latter', 'latterly', 'least', 'less', 'ltd', 'made']
stopwords += ['many', 'may', 'me', 'meanwhile', 'might', 'mill', 'mine']
stopwords += ['more', 'moreover', 'most', 'mostly', 'move', 'much']
stopwords += ['must', 'my', 'myself', 'name', 'namely', 'neither', 'never']
stopwords += ['nevertheless', 'next', 'nine', 'no', 'nobody', 'none']
stopwords += ['noone', 'nor', 'not', 'nothing', 'now', 'nowhere', 'of']
stopwords += ['off', 'often', 'on', 'once', 'one', 'only', 'onto', 'or']
stopwords += ['other', 'others', 'otherwise', 'our', 'ours', 'ourselves']
stopwords += ['out', 'over', 'own', 'part', 'per', 'perhaps', 'please']
stopwords += ['put', 'rather', 're', 's', 'same', 'see', 'seem', 'seemed']
stopwords += ['seeming', 'seems', 'serious', 'several', 'she', 'should']
stopwords += ['show', 'side', 'since', 'sincere', 'six', 'sixty', 'so']
stopwords += ['some', 'somehow', 'someone', 'something', 'sometime']
stopwords += ['sometimes', 'somewhere', 'still', 'such', 'system', 'take']
stopwords += ['ten', 'than', 'that', 'the', 'their', 'them', 'themselves']
stopwords += ['then', 'thence', 'there', 'thereafter', 'thereby']
stopwords += ['therefore', 'therein', 'thereupon', 'these', 'they']
stopwords += ['thick', 'thin', 'third', 'this', 'those', 'though', 'three']
stopwords += ['three', 'through', 'throughout', 'thru', 'thus', 'to']
stopwords += ['together', 'too', 'top', 'toward', 'towards', 'twelve']
stopwords += ['twenty', 'two', 'un', 'under', 'until', 'up', 'upon']
stopwords += ['us', 'very', 'via', 'was', 'we', 'well', 'were', 'what']
stopwords += ['whatever', 'when', 'whence', 'whenever', 'where']
stopwords += ['whereafter', 'whereas', 'whereby', 'wherein', 'whereupon']
stopwords += ['wherever', 'whether', 'which', 'while', 'whither', 'who']
stopwords += ['whoever', 'whole', 'whom', 'whose', 'why', 'will', 'with']
stopwords += ['within', 'without', 'would', 'yet', 'you', 'your']
stopwords += ['yours', 'yourself', 'yourselves']

highest_word_count = defaultdict(int)
all_words = defaultdict(int)


# Function for #2
def word_count_checker(url):
    global highest_word_count
    global stopwords
    unique_words = set()
    page = urlopen(url)
    soup = BeautifulSoup(page, 'html.parser')
    content = soup.get_text()

    # Split by non alphanumeric characters
    for token in re.split('[^a-zA-Z0-9]', content):
        # Check if token is alphanumeric, length is greater than one, and is not a stop
        if token.isalnum() and len(token) > 1 and token not in stopwords:
            # Add token to a set of unique words
            unique_words.add(token.lower())

    # Gets number of all unique tokens in the HTML content of the word page
    highest_word_count[url] = len(unique_words)


# Function for #3
def update_word_count(url):
    global all_words
    global stopwords
    page = urlopen(url)
    soup = BeautifulSoup(page, 'html.parser')
    content = soup.get_text()

    # Split by non alphanumeric characters
    for token in re.split('[^a-zA-Z0-9]', content):
        # Check if token is alphanumeric, length is greater than one, and is not a stop
        if token.isalnum() and len(token) > 1 and token not in stopwords:
            # Increment counter of token
            all_words[token.lower()] += 1


def top_50_common():
    # Top 50 common words (not sure if we can use Counter...)
    d = dict(all_words)
    counts = Counter(d)
    top_50_words = counts.most_common(50)
    return top_50_words


def ics_subdomains(url):

    subdomains = set()              # ex: subdomains = {"vision", "grape"}
    subdomain_pages = dict()        # ex: subdomain_pages = {"https://vision.ics.uci.edu": 10, "https://grape.ics.uci.edu": 20}

    # extract subdomain name
    parse = tldextract.extract(url)
    subdomain = parse.subdomain

    # if url contains "www", extract the name
    if "www" in subdomain:
        subdomain = subdomain[4:]

from urllib.parse import urlparse, urldefrag
from urllib.request import urlopen
from bs4 import BeautifulSoup
from collections import Counter
import html.parser
import utils
import re


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
            unique_pages.add(url)
            return True
        else:
            return False

    except TypeError:
        print("TypeError for ", parsed)
        raise


# Function for #2
def word_count_checker(url):
    page = urlopen(url)
    soup = BeautifulSoup(page, 'html.parser')
    content = soup.get_text()

    token_list = []
    for token in content:
        if not ((token >= '0' and token <= '9') 
            or (token >= 'A' and token <= 'Z')
            or (token >= 'a' and token <= 'z')):
             content = content.replace(token, ' ')
    token_list += content.lower().split()

    print(url, ':', len(token_list))


# Function for #3
def update_word_count(url):
    page = urlopen(url)
    soup = BeautifulSoup(page, 'html.parser')
    content = soup.get_text()

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
    stopwords += ['off', 'often', 'on','once', 'one', 'only', 'onto', 'or']
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

    # tokenize the text (reimplemented from assignment #1)
    token_list = []
    for token in content:
        if not ((token >= '0' and token <= '9') 
            or (token >= 'A' and token <= 'Z')
            or (token >= 'a' and token <= 'z')):
             content = content.replace(token, ' ')
    token_list += content.lower().split()

    # remove token with length < 2  
    token_list = [token for token in token_list if len(token) > 1]          
    # remove stopwords
    token_list = [token for token in token_list if token not in stopwords]   
        
    # Compute word frequency
    d = dict()
    for token in token_list:
        if not token in d:
            d[token] = 1
        else:
            d[token] = d[token] + 1     

    # Top 50 common words (not sure if we can use Counter...)
    counts = Counter(d)
    top_50_words = counts.most_common(50)
    
    return top_50_words 





subdomains = set()
# ex: subdomains = {"vision", "grape"}
subdomain_pages = dict()
# ex: subdomain_pages = {"https://vision.ics.uci.edu": 10, "https://grape.ics.uci.edu": 20}

def ics_subdomains(url):
    pass

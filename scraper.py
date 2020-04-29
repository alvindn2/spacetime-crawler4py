from urllib.parse import urlparse, urldefrag
from urllib.request import urlopen
from bs4 import BeautifulSoup
from collections import Counter, defaultdict
import pickle
import re


unique_paths = set()
unique_pages = set()                    # Keeps track of all unique pages
crawled_urls = set()                    # Keeps track of crawled urls
subdomains = set()                      # Keeps track of all subdomains
subdomain_pages = defaultdict(int)      # Keeps track of all unique pages per subdomain for ics.uci.edu
blacklist = set()                       # Keeps track of all urls that should be banned from accessing

longest_page_url = ""                   # Keeps track of page with most words
longest_page_word_count = 0             # Keeps track of the number of words of the largest file
all_words = defaultdict(int)            # Keeps track of all words and their frequencies


def scraper(url: str, resp):
    try:
        x = urlopen(url)
    except:
        #print("---HTTP Error in scraper(), skipping")
        return []

    # if is_valid(url) and x.getcode() == 200:
    if is_valid(url) and resp.status == 200:
        #print("\n\nCrawling...", url)
        defrag_url = urldefrag(url)[0]
        parsed = urlparse(defrag_url)
        host = parsed.hostname
        path = parsed.path
        unique_url = get_unique_page(url)
        unique_path = get_path_page(url)

        if ".ics.uci.edu/" in url:
            ics_subdomains(url)

        global unique_paths
        unique_paths.add(unique_path)
        global unique_pages
        unique_pages.add(unique_url)
        update_word_count(unique_url, resp)

        #print("Unique pages: ", len(unique_pages))
        #print("Subdomain_pages: ", {key: len(val) for key, val in subdomain_pages.items()})
        #print("Longest Page URL: ", longest_page_url)
        #print("Longest Word Count: ", longest_page_word_count)

        links = extract_next_links(defrag_url, resp)
        #print("Next links {}: {}".format(len(links), links))
        return [link for link in links]
    else:
        # print("\n---INVALID: ", url, x.getcode())
        return []


def extract_next_links(url, resp):
    global crawled_urls
    parsed = urlparse(url)
    host = parsed.hostname
    scheme = parsed.scheme

    links = []
    # page = urlopen(url)
    page = resp.resp.raw_response.content
    html_object = BeautifulSoup(page, "html.parser")
    for a_tag in html_object.find_all('a'):
        link = a_tag.get('href')
        if type(link) is not str:
            continue
        if link.startswith("//"):
            link = link[2:]
        elif link.startswith("/"):
            link = scheme+"://"+host+link
        if link not in unique_pages and link not in crawled_urls and is_valid(link):
            crawled_urls.add(link)
            links.append(link)
    return links


def is_valid(url):
    try:
        defrag_url = urldefrag(url)[0]
        parsed = urlparse(defrag_url)

        valid_hosts = [".ics.uci.edu/", ".cs.uci.edu/", ".informatics.uci.edu/", ".stat.uci.edu/",
                       "today.uci.edu/department/information_computer_sciences/"]
        valid_hostname = any(host in url for host in valid_hosts)

        valid_scheme = parsed.scheme in set(["http", "https"])

        poss_traps = ["/event/", "/events/", "calendar", "date", "gallery",
                      "image", "wp-content", "index.php", "upload", "?share=", "ical"]
        no_possible_traps = not any(trap in url for trap in poss_traps)

        no_extension = not re.match(
            r".*\.(css|js|bmp|gif|jpe?g|ico"
            + r"|png|tiff?|mid|mp2|mp3|mp4"
            + r"|wav|avi|mov|mpeg|ram|m4v|mkv|ogg|ogv|pdf"
            + r"|ps|eps|tex|ppt|pptx|doc|docx|xls|xlsx|names"
            + r"|data|dat|exe|bz2|tar|msi|bin|7z|psd|dmg|iso"
            + r"|epub|dll|cnf|tgz|sha1"
            + r"|thmx|mso|arff|rtf|jar|csv|odc"
            + r"|rm|smil|wmv|swf|wma|zip|rar|gz)$", parsed.path.lower())

        if not all([valid_hostname, valid_scheme, no_extension, no_possible_traps]):
            return False
        else:
            unique_path = get_path_page(url)
            if unique_path in unique_paths:
                forum_traps = ["#comment-", "?replytocom="]
                return not any(trap in url for trap in forum_traps)
            else:
                return True


        # return valid_hostname and valid_scheme and no_extension and no_possible_traps and no_forum_traps

    except TypeError:
        #print("TypeError for ", parsed)
        raise

# store the stopwords
stopwords = set()
stopwords.update(['a', 'about', 'above', 'across', 'after', 'afterwards'])
stopwords.update(['again', 'against', 'all', 'almost', 'alone', 'along'])
stopwords.update(['already', 'also', 'although', 'always', 'am', 'among'])
stopwords.update(['amongst', 'amoungst', 'amount', 'an', 'and', 'another'])
stopwords.update(['any', 'anyhow', 'anyone', 'anything', 'anyway', 'anywhere'])
stopwords.update(['are', 'around', 'as', 'at', 'back', 'be', 'became'])
stopwords.update(['because', 'become', 'becomes', 'becoming', 'been'])
stopwords.update(['before', 'beforehand', 'behind', 'being', 'below'])
stopwords.update(['beside', 'besides', 'between', 'beyond', 'bill', 'both'])
stopwords.update(['bottom', 'but', 'by', 'call', 'can', 'cannot', 'cant'])
stopwords.update(['co', 'computer', 'con', 'could', 'couldnt', 'cry', 'de'])
stopwords.update(['describe', 'detail', 'did', 'do', 'done', 'down', 'due'])
stopwords.update(['during', 'each', 'eg', 'eight', 'either', 'eleven', 'else'])
stopwords.update(['elsewhere', 'empty', 'enough', 'etc', 'even', 'ever'])
stopwords.update(['every', 'everyone', 'everything', 'everywhere', 'except'])
stopwords.update(['few', 'fifteen', 'fifty', 'fill', 'find', 'fire', 'first'])
stopwords.update(['five', 'for', 'former', 'formerly', 'forty', 'found'])
stopwords.update(['four', 'from', 'front', 'full', 'further', 'get', 'give'])
stopwords.update(['go', 'had', 'has', 'hasnt', 'have', 'he', 'hence', 'her'])
stopwords.update(['here', 'hereafter', 'hereby', 'herein', 'hereupon', 'hers'])
stopwords.update(['herself', 'him', 'himself', 'his', 'how', 'however'])
stopwords.update(['hundred', 'i', 'ie', 'if', 'in', 'inc', 'indeed'])
stopwords.update(['interest', 'into', 'is', 'it', 'its', 'itself', 'keep'])
stopwords.update(['last', 'latter', 'latterly', 'least', 'less', 'ltd', 'made'])
stopwords.update(['many', 'may', 'me', 'meanwhile', 'might', 'mill', 'mine'])
stopwords.update(['more', 'moreover', 'most', 'mostly', 'move', 'much'])
stopwords.update(['must', 'my', 'myself', 'name', 'namely', 'neither', 'never'])
stopwords.update(['nevertheless', 'next', 'nine', 'no', 'nobody', 'none'])
stopwords.update(['noone', 'nor', 'not', 'nothing', 'now', 'nowhere', 'of'])
stopwords.update(['off', 'often', 'on', 'once', 'one', 'only', 'onto', 'or'])
stopwords.update(['other', 'others', 'otherwise', 'our', 'ours', 'ourselves'])
stopwords.update(['out', 'over', 'own', 'part', 'per', 'perhaps', 'please'])
stopwords.update(['put', 'rather', 're', 's', 'same', 'see', 'seem', 'seemed'])
stopwords.update(['seeming', 'seems', 'serious', 'several', 'she', 'should'])
stopwords.update(['show', 'side', 'since', 'sincere', 'six', 'sixty', 'so'])
stopwords.update(['some', 'somehow', 'someone', 'something', 'sometime'])
stopwords.update(['sometimes', 'somewhere', 'still', 'such', 'system', 'take'])
stopwords.update(['ten', 'than', 'that', 'the', 'their', 'them', 'themselves'])
stopwords.update(['then', 'thence', 'there', 'thereafter', 'thereby'])
stopwords.update(['therefore', 'therein', 'thereupon', 'these', 'they'])
stopwords.update(['thick', 'thin', 'third', 'this', 'those', 'though', 'three'])
stopwords.update(['three', 'through', 'throughout', 'thru', 'thus', 'to'])
stopwords.update(['together', 'too', 'top', 'toward', 'towards', 'twelve'])
stopwords.update(['twenty', 'two', 'un', 'under', 'until', 'up', 'upon'])
stopwords.update(['us', 'very', 'via', 'was', 'we', 'well', 'were', 'what'])
stopwords.update(['whatever', 'when', 'whence', 'whenever', 'where'])
stopwords.update(['whereafter', 'whereas', 'whereby', 'wherein', 'whereupon'])
stopwords.update(['wherever', 'whether', 'which', 'while', 'whither', 'who'])
stopwords.update(['whoever', 'whole', 'whom', 'whose', 'why', 'will', 'with'])
stopwords.update(['within', 'without', 'would', 'yet', 'you', 'your'])
stopwords.update(['yours', 'yourself', 'yourselves'])


# Function for #2
def update_word_count(url, resp):
    global all_words
    global longest_page_url
    global longest_page_word_count
    global stopwords
    unique_words = set()
    word_counter = 0

    try:
        # page = urlopen(url)
        page = resp.raw_response.content
        soup = BeautifulSoup(page, 'html.parser')
        content = soup.get_text()

        # Split by non alphanumeric characters
        for token in re.split('[^a-zA-Z0-9]', content):
            # Check if token is alphanumeric, length is greater than one, and is not a stop
            if token.isalnum() and len(token) > 2 and token not in stopwords:
                # Add token to a set of unique words
                unique_words.add(token.lower())

                # Increment word counter of file
                word_counter += 1

                # Increment counter of token
                all_words[token.lower()] += 1

        # Means that there cannot be 10x as many total words as there are unique words in a file.
        few_duplicates = (word_counter/len(unique_words)) < 10
        # Checks to make sure there are at least 100 words in a file, not too low information
        large_word_count = word_counter > 50
        # Checks if the number of words is larger than current largest file
        larger_than_best = word_counter > longest_page_word_count

        if few_duplicates and large_word_count and larger_than_best:
            longest_page_url = url
            longest_page_word_count = word_counter

    except:
        # print("---HTTP Error in update_word_count(), skipping")
        pass


def top_50_common():
    # Top 50 common words (not sure if we can use Counter...)
    d = dict(all_words)
    counts = Counter(d)
    top_50_words = counts.most_common(50)
    return top_50_words


def ics_subdomains(url):
    # global subdomains           # ex: subdomains = {"vision", "grape"}
    global subdomain_pages      # ex: subdomain_pages = {"https://vision.ics.uci.edu": {}}

    # extract subdomain name
    parse = urlparse(url)
    subdomain = parse.hostname.split(".ics.uci.edu")[0]

    # if url contains "www", extract the name
    if "www." in subdomain:
        subdomain = subdomain[4:]

    # subdomains.add(subdomain)

    unique_page_url = get_unique_page(url)
    if unique_page_url not in unique_pages:
        subdomain_pages[subdomain] += 1


def get_unique_page(url):
    return urldefrag(url)[0]

def get_path_page(url):
    parse = urlparse(url)
    return parse.scheme + "://" + parse.hostname + parse.path

def print_report():
    print("--------------- CS 121 Report ---------------")
    print()
    print("Team: Alvin Nguyen [80452034], Paul Le [62609666], Bao Duy Ly [72926167] ")
    print()
    print("Number of Unique URLs:", len(unique_pages))
    print()
    print("Longest URL:", longest_page_url)
    print("Word Count:", longest_page_word_count)
    print()

    print("50 Most Common Words:")
    counter = 1
    for key, value in sorted(all_words.items(), key=lambda x: x[1], reverse=True):
        if counter <= 50:
            print(str(counter) + ". " + key + " (" + str(value) + ")")
            counter = int(counter)
            counter += 1
        else:
            break
    print()
    print("Subdomains in ics.uci.edu:")
    for subdomain, val in sorted(subdomain_pages.items(), key=lambda x: x[0], reverse=True):
        print(subdomain + ": " + str(val))
    print()
    print("--------------- CS 121 Report ---------------")

# if __name__ == "__main__":
#     counter = 1
#     frontier = ["https://www.ics.uci.edu/", "https://www.cs.uci.edu/",
#                 "https://www.informatics.uci.edu/", "https://www.stat.uci.edu/",
#                 "https://today.uci.edu/department/information_computer_sciences/"]
#     while counter < 1000:
#         l = frontier.pop(0)
#         frontier.extend(scraper(l, 200))
#         # print("Frontier: {}".format(frontier[1:]))
#         counter += 1
#
#     print("--------------- CS 121 Report ---------------")
#     print()
#     print("Team: Alvin Nguyen [80452034], Paul Le [62609666], Bao Duy Ly [72926167] ")
#     print()
#     print("Number of Unique URLs:", len(unique_pages))
#     print()
#     print("Longest URL:", longest_page_url)
#     print("Word Count:", longest_page_word_count)
#     print()
#
#     print("50 Most Common Words:")
#     counter = 1
#     for key, value in sorted(all_words.items(), key=lambda x: x[1], reverse=True):
#         if counter <= 50:
#             print(str(counter) + ". " + key + " (" + str(value) + ")")
#             counter = int(counter)
#             counter += 1
#         else:
#             break
#     print()
#     print("Subdomains in ics.uci.edu:")
#     for subdomain, val in sorted(subdomain_pages.items(), key=lambda x: x[0], reverse=True):
#         print(subdomain + ": " + val)
#     print()
#     print("--------------- CS 121 Report ---------------")
#
#     # write unique pages into text
#     with open('up.data', 'wb') as up:
#         pickle.dump(unique_pages, up)
#
#     # write longest page into text
#     with open('lp.data', 'wb') as lp:
#         pickle.dump(longest_page_url, lp)
#
#     # write common words into text
#     with open('cw.data', 'wb') as cw:
#         pickle.dump(top_50_common(), cw)
#
#     # write subdomains and unique pages into text
#     with open('sp.data', 'wb') as sp:
#         pickle.dump(subdomain_pages, sp)
#
#     ##############################
#     #  Printing out information  #
#     ##############################
#
#     # load unique pages
#     with open('up.data', 'rb') as up:
#         load_up = pickle.load(up)
#         print(load_up)
#
#     # load longest page
#     with open('lp.data', 'rb') as lp:
#         load_lp = pickle.load(lp)
#         print(load_lp)
#
#     # load common words
#     with open('cw.data', 'rb') as cw:
#         load_cw = pickle.load(cw)
#         print(load_cw)
#
#     # load subdomains and unique pages
#     with open('sp.data', 'rb') as sp:
#         load_sp = pickle.load(sp)
#         print(load_sp)

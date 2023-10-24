import re
from collections import defaultdict

import lxml
from urllib.parse import urlparse
from bs4 import BeautifulSoup

def scraper(url, resp):
    try:
        links = extract_next_links(url, resp)
        return [link for link in links if is_valid(link)]
    except AttributeError as e:
        print(e)


def extract_next_links(url, resp):
    # Implementation required.
    # url: the URL that was used to get the page
    # resp.url: the actual url of the page
    # resp.status: the status code returned by the server. 200 is OK, you got the page. Other numbers mean that there was some kind of problem.
    # resp.error: when status is not 200, you can check the error here, if needed.
    # resp.raw_response: this is where the page actually is. More specifically, the raw_response has two parts:
    #         resp.raw_response.url: the url, again
    #         resp.raw_response.content: the content of the page!
    # Return a list with the hyperlinks (as strings) scrapped from resp.raw_response.content


    '''
    Citations: https://pythonprogramminglanguage.com/get-links-from-webpage/
    '''

    hyperlinks = []
    unwantedTags = ["img", "nav"]

    # checks if the response status code is 200 and the content of the page is not empty
    if resp is not None and resp.raw_response.content:
        if resp.status == 200:
            try:

                soupObj = BeautifulSoup(resp.raw_response.content,'lxml')  # using beautiful soup with lxml parser for better performance

                #scraping hyperlinks in webpage
                potentialHyperLinks = soupObj.find_all('a')  # 'a' tag doesn't neccesarily mean hyperlink is present. must check for 'a tag with href attribute'
                for data in potentialHyperLinks:
                    hyperlinks.append(data.get("href"))  # Citation Above. Noticed finding all a-tags doesn't provide just hyperlinks, so learned and implemented going line by line to check for href attributes

                #scraping all text in webpage for computation of number of words, common words, etc.
                webPageTags = soupObj.find_all()
                for tags in webPageTags:
                    


                return list(hyperlinks)
            except AttributeError as e:
                print(e)
    print("resp was None")
    return list(hyperlinks)


def is_valid(url):
    # Decide whether to crawl this url or not. 
    # If you decide to crawl it, return True; otherwise return False.
    # There are already some conditions that return False.

    try:
        parsed = urlparse(url)
        if parsed.scheme not in set(["http", "https"]):
            # print("failed at scheme")
            return False

        # Check if the domain is within the allowed domains
        allowed_domains = ["www.ics.uci.edu", "www.cs.uci.edu", "www.informatics.uci.edu", "www.stat.uci.edu"]
        if parsed.netloc not in allowed_domains:
            # print("failed at domain")
            return False

        # Check if the URL has a fragment identifier
        if "#" in parsed.fragment:
            # Extract the URL without the fragment identifier
            url_without_fragment = parsed.geturl()[:parsed.geturl().rfind("#")]

            # Check if the URL without the fragment has been visited
            # url.frontier.to_be_downloaded is a list in frontier.py that stores all visited urls
            if url_without_fragment in url.frontier.to_be_downloaded: #need to cut down url to only without fragment?
                return False
                # print("failed at fragment")
            else:
                # Mark the URL without the fragment as visited
                url.frontier.to_be_downloaded.add(url_without_fragment)

        #if not parsed.path.startswith("/"):
        #    return False

        # TRAP CHECKING
        # Check for common traps in the path
        path_traps = ["/calendar", "/ical", "/redirect", "/session", "/logout", "/search", "/user/", "/error",
                   "/archive", "/sitemap", "/login", "/auth", "/404"]
        for trap in path_traps:
            if trap in parsed.path:
                print("Found trap:", trap)
                return False

        # Check for common traps in the query
        query_traps = ["session=", "timestamp=", "ts="]
        for trap in query_traps:
            if trap in parsed.query:
                print("Found trap:", trap)
                return False


        # Check for invalid file extensions
        return not re.match(
            r".*\.(css|js|bmp|gif|jpe?g|ico"
            + r"|png|tiff?|mid|mp2|mp3|mp4"
            + r"|wav|avi|mov|mpeg|ram|m4v|mkv|ogg|ogv|pdf"
            + r"|ps|eps|tex|ppt|pptx|doc|docx|xls|xlsx|names"
            + r"|data|dat|exe|bz2|tar|msi|bin|7z|psd|dmg|iso"
            + r"|epub|dll|cnf|tgz|sha1"
            + r"|thmx|mso|arff|rtf|jar|csv"
            + r"|rm|smil|wmv|swf|wma|zip|rar|gz)$", parsed.path.lower())

    except TypeError:
        print ("TypeError for ", parsed)
        raise

    return true



def tokenizer(text):
    tokens = re.findall(r'[a-zA-Z0-9]+', text.lower())
    return tokens

def countWordsOnPage():
    pass

def computeWordFrequencies(tokensList):
    token_count = defaultdict(int)
    for token in tokensList:
        token_count[token] += 1




# Testing:
url = "http://www.ics.uci.edu/calendar/"
if is_valid(url):
    print("This URL is valid.")
else:
    print("This URL is not valid.")


# TODO 1. pdfs
# TODO 2. if a response is none we need to gtfo instead of pass none.content bc that throws an exception
# TODO remove id as a trap?
# todo fragment checker might not be matching any urls since the link at hand has fragment removed but the list in
#  the frontier is the entire link. can fix by having a loop outside the try where each url.frontier.to.be.downloaded
#  has its pre-fragment removed so that the "in" will produce matches
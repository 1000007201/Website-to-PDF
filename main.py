import requests
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup
import pdfkit





# initialize the set of links (unique links)
internal_urls = set()
external_urls = set()

total_urls_visited = 0


def is_valid(url):
    """
    Checks whether `url` is a valid URL.
    """
    parsed = urlparse(url)
    return bool(parsed.netloc) and bool(parsed.scheme)


def get_all_website_links(url):


    urls = set()
    # domain name of the URL without the protocol
    domain_name = urlparse(url).netloc
    soup = BeautifulSoup(requests.get(url).content, "html.parser")
    for a_tag in soup.findAll("a"):
        href = a_tag.attrs.get("href")
        if href == "" or href is None:
            # href empty tag
            continue
        # joining the URL's
        href = urljoin(url, href)
        parsed_href = urlparse(href)
        # remove URL GET parameters, URL fragments, etc.
        href = parsed_href.scheme + "://" + parsed_href.netloc + parsed_href.path
        if not is_valid(href):
            # not a valid URL
            continue
        if href in internal_urls:
            # already in the set
            continue
        if domain_name not in href:
            # external link
            if href not in external_urls:
                print(f"[!] External link: {href}")
                external_urls.add(href)
            continue
        print(f"[*] Internal link: {href}")
        urls.add(href)
        internal_urls.add(href)
    return urls

try:
    def crawl(url, max_urls=50):

        global total_urls_visited
        total_urls_visited += 1
        links = get_all_website_links(url)
        for link in links:
            if total_urls_visited > max_urls:
                break
            crawl(link, max_urls=50)
except Exception as e:
    print(e)

if __name__ == "__main__":

    url = "https://cbdbene.com"
    max_urls = 50

    crawl(url, max_urls=50)

    print("[+] Total Internal links:", len(internal_urls))
    print("[+] Total External links:", len(external_urls))
    print("[+] Total URLs:", len(external_urls) + len(internal_urls))

    domain_name = urlparse(url).netloc
    # print(internal_urls)

    # save the internal links to a file
    with open(f"{domain_name}_internal_links.txt", "w") as f:
        for internal_link in internal_urls:
            print(internal_link.strip(), file=f)

    # save the external links to a file
    with open(f"{domain_name}_external_links.txt", "w") as f:
        for external_link in external_urls:
            print(external_link.strip(), file=f)


with open('cbdbene.com_internal_links.txt') as x:
    b = [word for line in x for word in line.split()]
    # print(b)

path_wkhtmltopdf = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'

config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)
# Saving pdf of website in file test1
pdfkit.from_url(b, r"E:\Scripting\export\test1.pdf",configuration = config)
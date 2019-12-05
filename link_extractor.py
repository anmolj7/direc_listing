from bs4 import BeautifulSoup
import requests
import re 

class LinkExtractor:

    def is_link_valid(self, url):
        #First type is the one, which is like /home /cookie-policy etc.
        if not url:
            return False 

        url = url.replace("https://", "").replace("http://", "")
        if url[0] == '/':
            return True

        base_url = self.url 
        base_url = base_url.replace("https://", "").replace("http://", "")

        i = re.search(".com", base_url)
        j = re.search(".com", url)

        if i != None and j != None:
            #Second is the conventail one, like domain.com/direc
            if url[:i.start()] == base_url[:j.start()]:
                return True 

        return False 
    def extract_links(self, url):
        print(f"Extracting links from {url}")
        self.url = url 
        html_page = requests.get(url).content
        soup = BeautifulSoup(html_page, "lxml")
        urls = []
        for link in soup.findAll('a'):
            urls += [link.get("href")]
        
        #Filtering links
        urls = [url for url in urls if self.is_link_valid(url)]
        #Removing duplicates..
        urls = list(set(urls))
        return urls if len(urls) else None 
    
    def GetAllLinks(self, base_url):
        Links = []
        self.get_all_links(base_url, Links, [])
        return list(set(Links))

    #Utility function.
    def get_all_links(self, base_url: str, global_extracted_urls: list, crawled_urls: list):
        '''
        Recursive approach to find extract all the possible urls.
        '''

        #Base case
        curr_extracted_urls = self.extract_links(base_url)
        if len(curr_extracted_urls) == 0:
            global_extracted_urls += [base_url]
            global_extracted_urls = list(set(global_extracted_urls))
            return
        
        #Recursive case.
        for url in curr_extracted_urls:
            if url not in crawled_urls:
                crawled_urls.append(url)
                global_extracted_urls.append(url)
                temp_urls = []
                self.get_all_links(url, temp_urls, crawled_urls)
                global_extracted_urls += temp_urls
                global_extracted_urls = list(set(global_extracted_urls))

    def DirectoryExtractor(self, urls: list):
        regex = re.compile(
            r'^(?:http|ftp)s?://' # http:// or https://
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
            r'localhost|' #localhost...
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
            r'(?::\d+)?' # optional port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)
        Directories = []
        for url in urls:
            direcs = url.split('.com')[1].strip('/').split('/')
            for direc in direcs:
                Directories.append(url[:url.index(direc)+1+len(direc)])
        Directories = [direc for direc in Directories if re.match(regex, direc) is not None]
        return list(set(Directories))

def is_vuln(url):
    try:
        soup = BeautifulSoup(requests.get(url).content, "lxml")
    except:
        soup = BeautifulSoup(requests.get(url).content)
    h1 = soup.find("h1")
    if "Index of" in h1.text:
        return True 
    return False

if __name__ == "__main__":
    #url = "https://pythonspot.com/extract-links-from-webpage-beautifulsoup/"
    url = "https://codingwithaj.blogspot.com/"
    link_extractor = LinkExtractor()
    Links = link_extractor.GetAllLinks(url)
    print(link_extractor.DirectoryExtractor(Links))
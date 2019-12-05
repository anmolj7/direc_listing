from link_extractor import LinkExtractor, is_vuln

def main():
    url = input("Enter the url of the website including the protocol, example(https://example.com): ")
    if is_vuln(url):
        print("The website is vulnerable at", url)
    else:
        Links = LinkExtractor().GetAllLinks(url)
        Direcs = LinkExtractor().DirectoryExtractor(Links)
        print('-'*60)
        print('All Links Extracted.')
        print('-'*60)
        print("Checking vulnerablities.")
        safe = True 
        for direc in Direcs:
            print(f"Checking if the site is vulnerable at {direc}")
            if is_vuln(direc):
                safe = False
                print(f"The website is vulnerable at: {direc}")
        if safe:
            print("The website is secure (Atleast of directory listing vulns).")

if __name__ == "__main__":
    main()
from selenium import webdriver
from selenium.common.exceptions import ElementClickInterceptedException, NoSuchElementException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from multiprocessing import Manager
from abc import ABC, abstractmethod
from time import sleep

class Scraper(ABC):

    def __init__(self, options: Options, service: Service):
        self.driver = webdriver.Chrome(service=service,
                                options=options)
        self.driver.set_window_size(1280, 720)
        self.queryCache = Manager().dict()
        self.BASE_URL = ""

    def resetToBaseUrl(self):
        print('resetting to baseurl')
        print(f"base url: {self.BASE_URL}, query cache: {self.queryCache}")
        self.driver.get(self.BASE_URL)
        if 'location' in self.queryCache:
            self.setLocation(self.queryCache['location'])
        if 'query' in self.queryCache:
            self.search(self.queryCache['query'])

    @abstractmethod
    def _getListings(self):
        pass

    @abstractmethod
    def setLocation(self, location: str):
        pass

    @abstractmethod
    def search(self, query: str):
        pass

    @abstractmethod
    def getBasicInfo(self, returnDict: dict):
        pass

    @abstractmethod
    def getJobPoints(self, returnDict: dict):
        pass

class NodeFlairScraper(Scraper):
    def __init__(self, options: Options, service: Service):
        super().__init__(options, service)
        self.BASE_URL = "https://nodeflair.com/jobs?query=&page=1&sort_by=relevant&countries%5B%5D=Singapore"
        self.driver.get(self.BASE_URL)
        self.driver.implicitly_wait(10)
        self.NAME = 'NodeFlair'

        self.VALID_COUNTRIES = {'Singapore', 'Malaysia', 'Phillipines', 'Indonesia', 'Vietnam', 'Thailand', 'Taiwan', 'India'}

    def _getListings(self):
        activeItem = self.driver.find_element(By.XPATH, "//div[@class='jobListingCard-0-3-79 outlinePrimary-0-3-80']")
        return [activeItem] + self.driver.find_elements(By.XPATH, "//div[@class='jobListingCard-0-3-79 ']")
    
    def setLocation(self, location: str):
        if location.title() not in self.VALID_COUNTRIES:
            return 

        self.queryCache['location'] = location
        query = self.queryCache['query'] if 'query' in self.queryCache else ""
        self.driver.get(f"https://nodeflair.com/jobs?query={query}&page=1&sort_by=relevant&countries%5B%5D={location.title()}")
    
    def search(self, query:str):
        self.queryCache['query'] = query
        searchbar = self.driver.find_element(By.XPATH, "//input[@class='react-autosuggest__input']")
        # I honestly don't know why clear() doesn't work here but it just doesn't lmao
        for _ in range(50):
            searchbar.send_keys(Keys.BACK_SPACE)
        searchbar.send_keys(query)
        searchbar.send_keys(Keys.RETURN)

    def getBasicInfo(self, returnDict: dict):
        self.listings = self._getListings()

        res = []
        for listing in self.listings:
            title = listing.find_element(By.XPATH, ".//h2[@class='jobListingCardTitle-0-3-82']").text
            company = listing.find_element(By.XPATH, ".//p[@class='companynameAndRating-0-3-92']/span[1]").text
            link = listing.find_element(By.XPATH, "./a").get_attribute("href")
            res.append({
                "title": title,
                "company": company,
                "link": link
            })
        
        returnDict[self.NAME] = res

    def getJobPoints(self, returnDict: dict):
        self.listings = self._getListings()

        res = []
        def getCurrJobPoints():
            pts = self.driver.find_elements(By.XPATH, "//div[@class='jobDescriptionContent-0-3-121']//li")
            return list(map(lambda x: x.text, pts))

        for listing in self.listings:
            listing.click()
            res.extend(getCurrJobPoints())

        returnDict[self.NAME] = res
        self.resetToBaseUrl()

class LinkedinScraper(Scraper):
    def __init__(self, options: Options, service: Service):
        super().__init__(options, service)
        self.BASE_URL = "https://www.linkedin.com/jobs/search"
        self.driver.get(self.BASE_URL)
        self.driver.implicitly_wait(10)
        self.NAME = 'LinkedIn'

    def _getListings(self):
        activeListing = self.driver.find_element(By.XPATH, "//div[@class='base-card relative w-full hover:no-underline focus:no-underline base-card--link base-search-card base-search-card--link job-search-card job-search-card--active']")
        otherListings = self.driver.find_elements(By.XPATH, "//div[@class='base-card relative w-full hover:no-underline focus:no-underline base-card--link base-search-card base-search-card--link job-search-card']")
        return [activeListing, *otherListings]


    def setLocation(self, location: str):
        self.queryCache['location'] = location
        countrySearchBar = self.driver.find_element(By.XPATH, "//input[@id='job-search-bar-location']")
        countrySearchBar.clear()
        countrySearchBar.send_keys(location)
        countrySearchBar.send_keys(Keys.RETURN)

    
    def search(self, query:str):
        self.queryCache['query'] = query
        searchBar = self.driver.find_element(By.XPATH, "//input[@id='job-search-bar-keywords']")
        searchBar.clear()
        searchBar.send_keys(query) 
        searchBar.send_keys(Keys.RETURN)

    def getBasicInfo(self, returnDict: dict):
        self.listings = self._getListings()

        res = []
        for listing in self.listings:
            title = listing.find_element(By.XPATH, ".//h3[@class='base-search-card__title']").text
            company = listing.find_element(By.XPATH, ".//h4[@class='base-search-card__subtitle']").text 
            link = listing.find_element(By.XPATH, "./a").get_attribute("href")
            res.append({
                "title": title,
                "company": company,
                "link": link
            })

        returnDict[self.NAME] = res

    def getJobPoints(self, returnDict: dict):
        # linkedin blocks headless browsers / non logged in users from accessing JDs
        pass

class GlintsScraper(Scraper):
    def __init__(self, options: Options, service: Service):
        super().__init__(options, service)
        self.BASE_URL = "https://glints.com/sg/opportunities/jobs/explore?country=SG&locationName=All+Cities%2FProvinces&keyword=intern"
        self.driver.get(self.BASE_URL)
        self.driver.implicitly_wait(10)

        self.NAME = 'Glints'
        self.VALID_COUNTRIES = {'Singapore',
                                'Malaysia',
                                'Phillipines',
                                'Indonesia',
                                'Vietnam',
                                'Thailand',
                                'Taiwan',
                                'India',
                                'Hong Kong',
                                'China',
                                'Japan',
                                'Australia',
                                'United States'}

    def _getListings(self):
        def extractLink(listing):
            return listing.find_element(By.XPATH, "./div/a").get_attribute('href')
        sleep(2)
        listingsWithoutLinks = self.driver.find_elements(By.XPATH, "//div[@class='JobCardsc__JobcardContainer-sc-hmqj50-0 iirqVR CompactOpportunityCardsc__CompactJobCardWrapper-sc-dkg8my-0 dwwanr compact_job_card']")[:10]
        sleep(2)
        return list(map(lambda l: [l, extractLink(l)], listingsWithoutLinks))

    def setLocation(self, location: str):
        if location not in self.VALID_COUNTRIES:
            return

        self.queryCache['location'] = location
        countryInput = self.driver.find_element(By.XPATH, "//div[@class='SelectStyle__SelectWrapper-sc-gv8n2w-1 driwsF select-inputwrapper']")
        countryInput.click()
        countrySelect = self.driver.find_element(By.XPATH, "//ul[@class='SelectStyle__SelectListWrapper-sc-gv8n2w-4 hNAXQP select-listbox']")
        selectedCountry = countrySelect.find_element(By.XPATH, f".//li[contains(text(), '{location}')]")
        selectedCountry.click()
    
    def search(self, query:str):
        self.queryCache['query'] = query
        url = self.driver.current_url
        currSearchQueryIdx = url.index('&keyword=') + len('&keyword=')
        self.driver.get(url[:currSearchQueryIdx] + query)

    def getBasicInfo(self, returnDict: dict):
        self.listings = self._getListings()

        res = []
        for l in self.listings:
            listing = l[0]
            title = listing.find_element(By.XPATH, ".//h3[@class='CompactOpportunityCardsc__JobTitle-sc-dkg8my-7 hDhBMu']").text
            company = listing.find_element(By.XPATH, ".//span[@class='CompactOpportunityCardsc__CompanyLinkContainer-sc-dkg8my-10 hMaaBr']").text
            link = l[1]
            res.append({
                "title": title,
                "company": company,
                "link": link
            })

        returnDict[self.NAME] = res

    def getJobPoints(self, returnDict: dict):
        self.listings = self._getListings()

        res = []

        def extractInfo():
            try:
                readMoreBtn = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Read More')]")
                readMoreBtn.click()
            except NoSuchElementException:
                pass
            desc = self.driver.find_element(By.XPATH, "//div[@class='public-DraftEditor-content']")
            pts = desc.find_elements(By.XPATH, ".//li//span[@data-text='true']")
            return list(map(lambda x: x.text, pts))

        for l in self.listings:
            link = l[1]
            self.driver.get(link)
            try:
                res.extend(extractInfo())
            except ElementClickInterceptedException:
                # the popup is in the way lmao
                print('skipped element')
            self.driver.back()
        
        returnDict[self.NAME] = res
        self.resetToBaseUrl()

class InternSgScraper(Scraper):
    def __init__(self, options: Options, service: Service):
        super().__init__(options, service)
        self.BASE_URL = "https://www.internsg.com/jobs/"
        self.driver.get(self.BASE_URL)
        self.driver.implicitly_wait(10)
        self.NAME = 'InternSg'

    def _getListings(self):
        evenListings = self.driver.find_elements(By.XPATH, "//div[@class='ast-row list-even']")[:5]
        oddListings = self.driver.find_elements(By.XPATH, "//div[@class='ast-row list-odd']")[:5]
        return evenListings + oddListings


    def setLocation(self, location: str):
        # InternSG only serves singapore (obviously)
        pass
    
    def search(self, query:str):
        self.queryCache['query'] = query
        searchBar = self.driver.find_element(By.XPATH, "//input[@class='form-control form-control-sm']")
        searchBar.clear()
        searchBar.send_keys(query) 
        searchBar.send_keys(Keys.RETURN)

    def getBasicInfo(self, returnDict: dict):
        self.listings = self._getListings()

        res = []
        for listing in self.listings:
            title = listing.find_element(By.XPATH, "./div[2]/a").text
            company = listing.find_element(By.XPATH, "./div[1]").text 
            link = listing.find_element(By.XPATH, "./div[2]/a").get_attribute("href")
            res.append({
                "title": title,
                "company": company,
                "link": link
            })
        returnDict[self.NAME] = res

    def getJobPoints(self, returnDict: dict):
        self.listings = self._getListings()

        res = []

        def extractInfo():
            content = self.driver.find_element(By.XPATH, "//div[@class='isg-detail-container ast-row no-gutters']")
            pts = content.find_elements(By.XPATH, ".//li")
            parsedPts = list(map(lambda pt: pt.text, pts))
            res.extend(parsedPts)

        links = list(map(lambda l: l.find_element(By.XPATH, "./div[2]/a").get_attribute("href"), self.listings))
        for link in links:
            self.driver.get(link)
            extractInfo()
            self.driver.back()

        returnDict[self.NAME] = res
        self.resetToBaseUrl()

class GoogleScraper(Scraper):
    def __init__(self, options: Options, service: Service):
        super().__init__(options, service)
        self.BASE_URL = "https://www.google.com/search?q=intern&oq=sof&gs_lcrp=EgZjaHJvbWUqBggBEEUYOzIGCAAQRRg5MgYIARBFGDsyBggCEEUYOzIbCAMQLhgUGK8BGMcBGIcCGIAEGJgFGJkFGJ4FMhAIBBAuGMcBGLEDGNEDGIAEMgYIBRBFGEEyBggGEEUYPDIGCAcQRRg80gEIMzkzNGowajSoAgCwAgA&sourceid=chrome&ie=UTF-8&ibp=htl;jobs&sa=X&ved=2ahUKEwjYisWp4bWAAxU03jgGHb7WBSQQutcGKAF6BAgQEAY&sxsrf=AB5stBgAC-3yVvfOy8LZiInlqREPBQWxKQ:1690697051757#fpstate=tldetail&htivrt=jobs&htidocid=PnKDBGYnYJAAAAAAAAAAAA%3D%3D"
        self.driver.get(self.BASE_URL)
        self.driver.implicitly_wait(10)
        self.NAME = 'Google'

    def _getListings(self):
        return self.driver.find_elements(By.XPATH, "//li[@class='iFjolb gws-plugins-horizon-jobs__li-ed']")
    
    def setLocation(self, location: str):
        # Google careers automatically selects your location
        pass
    
    def search(self, query:str):
        self.queryCache['query'] = query
        searchbar = self.driver.find_element(By.ID, "hs-qsb")
        searchbar.clear()
        searchbar.send_keys(query)
        searchbar.send_keys(Keys.RETURN)

    def getBasicInfo(self, returnDict: dict):
        self.listings = self._getListings()

        res = []
        for listing in self.listings:
            title = listing.find_element(By.XPATH, ".//div[@class='BjJfJf PUpOsf']").text
            company = listing.find_element(By.XPATH, ".//div[@class='vNEEBe']").text
            res.append({
                "title": title,
                "company": company,
                "link": self.driver.current_url
            })
        
        returnDict[self.NAME] = res

    def getJobPoints(self, returnDict: dict):
        self.listings = self._getListings()

        res = []
        def getCurrJobPoints():
            text = self.driver.find_element(By.XPATH, "//span[@class='HBvzbc']").get_attribute('innerText')
            pts = text.split('\n')
            pts = [pt[2:] for pt in pts if pt and pt[0] == '•']
            return pts 

        for listing in self.listings:
            listing.click()
            res.extend(getCurrJobPoints())

        returnDict[self.NAME] = res
        self.resetToBaseUrl()
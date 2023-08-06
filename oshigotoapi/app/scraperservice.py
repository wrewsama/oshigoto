from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.utils import ChromeType
import app.scraper as scraper
from app.wordprocessor import WordProcessor

class ScraperService:
    def __init__(self):
        globalOptions = Options()
        globalOptions.add_experimental_option("detach", True)
        globalService = Service(
            ChromeDriverManager(
                chrome_type=ChromeType.CHROMIUM,
                version='114.0.5735.90').install())
        
        self.googleScraper = scraper.GoogleScraper(options=globalOptions, service=globalService)
        self.nodeflairScraper = scraper.NodeFlairScraper(options=globalOptions, service=globalService)
        self.linkedinScraper = scraper.LinkedinScraper(options=globalOptions, service=globalService)
        self.glintsScraper = scraper.GlintsScraper(options=globalOptions, service=globalService)
        self.internSgScraper = scraper.InternSgScraper(options=globalOptions, service=globalService)
        self.scrapers = [
            self.googleScraper,
            self.nodeflairScraper,
            self.linkedinScraper,
            # self.nodeflairScraper,
            # self.glintsScraper,
            # self.internSgScraper
        ]

    # TODO: make scraper methods async
    def search(self, query: str):
        for scraper in self.scrapers:
            scraper.search(query)

    def setLocation(self, location: str):
        for scraper in self.scrapers:
            scraper.setLocation(location)
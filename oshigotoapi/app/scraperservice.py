from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.utils import ChromeType
import app.scraper as scraper
from app.wordprocessor import WordProcessor
from multiprocessing import Process, Manager
from typing import Callable, Tuple

class ScraperService:
    def __init__(self):
        globalOptions = Options()
        globalOptions.add_experimental_option("detach", True)
        globalService = Service(
            ChromeDriverManager(
                chrome_type=ChromeType.CHROMIUM,
                version='114.0.5735.90').install())
        self.manager = Manager()
        self.processor = WordProcessor()
        
        self.googleScraper = scraper.GoogleScraper(options=globalOptions, service=globalService)
        self.nodeflairScraper = scraper.NodeFlairScraper(options=globalOptions, service=globalService)
        self.linkedinScraper = scraper.LinkedinScraper(options=globalOptions, service=globalService)
        self.glintsScraper = scraper.GlintsScraper(options=globalOptions, service=globalService)
        self.internSgScraper = scraper.InternSgScraper(options=globalOptions, service=globalService)
        self.scrapers = [
            self.googleScraper,
            self.nodeflairScraper,
            self.linkedinScraper,
            self.glintsScraper,
            self.internSgScraper
        ]
    def _runAllInParallel(self, fun: Callable, args: Tuple):
        processes = []
        for scraper in self.scrapers:
            process = Process(target=fun(scraper), args=args)
            process.start()
            processes.append(process)

        while processes:
            processes.pop().join()


    def search(self, query: str):
        searchFunction = lambda scraper: scraper.search
        self._runAllInParallel(searchFunction, (query, ))

    def setLocation(self, location: str):
        setFunction = lambda scraper: scraper.setLocation
        self._runAllInParallel(setFunction, (location, ))

    def getBasicInfo(self):
        returnDict = self.manager.dict()
        getFunction = lambda scraper: scraper.getBasicInfo
        self._runAllInParallel(getFunction, (returnDict, ))
        return returnDict

    def getTopJobPoints(self, count: int):
        returnDict = self.manager.dict()
        getFunction = lambda scraper: scraper.getJobPoints
        self._runAllInParallel(getFunction, (returnDict, )) 
        accumulatedPoints = []
        for scraper in returnDict:
            accumulatedPoints.extend(returnDict[scraper])
        res = self.processor.processData(accumulatedPoints, count)
        return res
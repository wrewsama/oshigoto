from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.utils import ChromeType
import scraper
from wordprocessor import WordProcessor
from multiprocessing import Process

if __name__ == '__main__':
    globalOptions = Options()
    globalOptions.add_experimental_option("detach", True)
    globalService = Service(
        ChromeDriverManager(
            chrome_type=ChromeType.CHROMIUM,
            version='114.0.5735.90').install())

    googleScraper = scraper.GoogleScraper(options=globalOptions, service=globalService)

    def nodeflair():
        nodeflairScraper = scraper.NodeFlairScraper(options=globalOptions, service=globalService)
        nodeflairScraper.setLocation('Singapore')
        nodeflairScraper.search('software engineer intern')
        nBasicInfo = nodeflairScraper.getBasicInfo()
        nJobPoints = nodeflairScraper.getJobPoints()
        print(f"NODEFLAIR BASIC INFO: {nBasicInfo}")
        print(f"NODEFLAIR JOB POINTS: {nJobPoints}")

    def linkedin():
        linkedinScraper = scraper.LinkedinScraper(options=globalOptions, service=globalService)
        linkedinScraper.setLocation("Singapore")
        linkedinScraper.search("software engineer intern")
        lBasicInfo = linkedinScraper.getBasicInfo()
        lJobPoints = linkedinScraper.getJobPoints()
        print(f"LINKEDIN BASIC INFO: {lBasicInfo}")
        print(f"LINKEDIN JOB POINTS: {lJobPoints}")

    def glints():
        glintsScraper = scraper.GlintsScraper(options=globalOptions, service=globalService)
        glintsScraper.search("Software engineer intern")
        glintsScraper.setLocation('India')
        gBasicInfo = glintsScraper.getBasicInfo()
        gJobPoints = glintsScraper.getJobPoints()
        print(f"GLINTS BASIC INFO: {gBasicInfo}")
        print(f"GLINTS JOB POINTS: {gJobPoints}")

    def internSg():
        internSgScraper = scraper.InternSgScraper(options=globalOptions, service=globalService)
        internSgScraper.search('Software engineer intern')
        iBasicInfo = internSgScraper.getBasicInfo()
        iJobPoints = internSgScraper.getJobPoints()
        print(f"INTERNSG BASIC INFO: {iBasicInfo}")
        print(f"INTERNSG JOB POINTS: {iJobPoints}")

    def google():
        googleScraper.search("software engineer intern")
        goBasicInfo = googleScraper.getBasicInfo()
        goJobPoints = googleScraper.getJobPoints()
        print(f"GOOGLE BASIC INFO: {goBasicInfo}")
        print(f"GOOGLE JOB POINTS: {goJobPoints}")

    nfProcess = Process(target=nodeflair)
    liProcess = Process(target=linkedin)
    glProcess = Process(target=glints)
    inProcess = Process(target=internSg)
    goProcess = Process(target=google)

    nfProcess.start()
    liProcess.start()
    glProcess.start()
    inProcess.start()
    goProcess.start()

    goProcess.join()
    inProcess.join()
    glProcess.join()
    liProcess.join()
    nfProcess.join()
    s = WordProcessor()
    test = [['The for construct iterates over the items in iterable', "while expression(item) provides"],
            ['Note that comprehensions can also have nested for clauses and conditional statements']]
    print(s.processData(test, 2))
    print("DONE")

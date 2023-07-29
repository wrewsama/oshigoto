from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.utils import ChromeType
import scraper

if __name__ == '__main__':
    globalOptions = Options()
    globalOptions.add_experimental_option("detach", True)
    globalService = Service(
        ChromeDriverManager(
            chrome_type=ChromeType.CHROMIUM,
            version='114.0.5735.90').install())

    # nodeflairScraper = scraper.NodeFlairScraper(options=globalOptions, service=globalService)
    # nodeflairScraper.setLocation('Singapore')
    # nodeflairScraper.search('software engineer intern')
    # basicInfo = nodeflairScraper.getBasicInfo()
    # jobPoints = nodeflairScraper.getJobPoints()
    # print(f"BASIC INFO: {basicInfo}")
    # print(f"JOB POINTS: {jobPoints}")

    # linkedinScraper = scraper.LinkedinScraper(options=globalOptions, service=globalService)
    # linkedinScraper.setLocation("Singapore")
    # linkedinScraper.search("software engineer intern")
    # # lbasicinfo = linkedinScraper.getBasicInfo()
    # lJobPts = linkedinScraper.getJobPoints()

    glintsScraper = scraper.GlintsScraper(options=globalOptions, service=globalService)
    glintsScraper.setLocation('India')
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.utils import ChromeType
import scraper

if __name__ == '__main__':
    globalOptions = Options()
    globalOptions.add_experimental_option("detach", True)
    globalService = Service(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install())

    # driver = webdriver.Chrome(service=Service(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install()),
    #                         options=options)
    # driver.set_window_size(1920, 1080)

    # nodeflairScraper = scraper.NodeFlairScraper(driver=driver)
    nodeflairScraper = scraper.NodeFlairScraper(options=globalOptions, service=globalService)
    nodeflairScraper.search('software engineer intern')
    basicInfo = nodeflairScraper.getBasicInfo()
    jobPoints = nodeflairScraper.getJobPoints()
    print(f"BASIC INFO: {basicInfo}")
    print(f"JOB POINTS: {jobPoints}")
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.utils import ChromeType
import scraper

if __name__ == '__main__':
    options = Options()
    options.add_experimental_option("detach", True)

    driver = webdriver.Chrome(service=Service(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install()),
                            options=options)

    nodeflairScraper = scraper.NodeFlairScraper(driver=driver)
    nodeflairScraper.search('software engineer intern')
    res = nodeflairScraper.getBasicInfo()
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from abc import ABC, abstractmethod

class Scraper(ABC):

    @abstractmethod
    def __init__(self, driver: webdriver.Chrome):
        self.driver = driver

    @abstractmethod
    def search(self, query: str):
        pass

class NodeFlairScraper(Scraper):
    def __init__(self, driver:webdriver.Chrome):
        self.driver = driver
        self.driver.get("https://nodeflair.com/jobs?countries%5B%5D=Singapore")
    
    def search(self, query:str):
        print(f'[INFO] search started with {query}')
        searchbar = self.driver.find_element(By.XPATH, "//input[@class='react-autosuggest__input']")
        searchbar.send_keys(query)
        searchbar.send_keys(Keys.RETURN)
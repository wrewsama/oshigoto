from selenium import webdriver
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
        print(f'search started with {query}')
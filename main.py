from bs4 import BeautifulSoup
import requests
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time

ZILLOW_URL = "https://www.zillow.com/san-francisco-ca/rentals/?searchQueryState=%7B%22mapBounds%22%3A%7B%22north%22%3A37.88538561080589%2C%22east%22%3A-122.23248568896484%2C%22south%22%3A37.66503410800981%2C%22west%22%3A-122.63417331103516%7D%2C%22isMapVisible%22%3Atrue%2C%22filterState%22%3A%7B%22price%22%3A%7B%22max%22%3A872627%7D%2C%22beds%22%3A%7B%22min%22%3A1%7D%2C%22fore%22%3A%7B%22value%22%3Afalse%7D%2C%22mp%22%3A%7B%22max%22%3A3000%7D%2C%22auc%22%3A%7B%22value%22%3Afalse%7D%2C%22nc%22%3A%7B%22value%22%3Afalse%7D%2C%22fr%22%3A%7B%22value%22%3Atrue%7D%2C%22fsbo%22%3A%7B%22value%22%3Afalse%7D%2C%22cmsn%22%3A%7B%22value%22%3Afalse%7D%2C%22fsba%22%3A%7B%22value%22%3Afalse%7D%7D%2C%22isListVisible%22%3Atrue%2C%22mapZoom%22%3A12%2C%22regionSelection%22%3A%5B%7B%22regionId%22%3A20330%2C%22regionType%22%3A6%7D%5D%2C%22pagination%22%3A%7B%7D%7D"
FORM_URL = "https://docs.google.com/forms/d/e/1FAIpQLSfrgRsSpUrhsRKvFnxaEI2DWh4OXx1gNa8cdyeLZs96p6NVtw/viewform?usp=sf_link"

# WEB scrapping using beautifully soup with narrowed search in zillow
# response = requests.get(ZILLOW_URL)
# response.raise_for_status()
# web_html = response.text
# soup = BeautifulSoup(web_html, "html.parser")
# print(soup.prettify())


class RentingResearchBot:

    def __init__(self):
        self.driver = webdriver.Firefox()
        self.rent_prices = []
        self.rent_links = []
        self.rent_address = []

    def get_rent_results(self):
        self.driver.get(ZILLOW_URL)
        time.sleep(2)
        self.rent_address = self.driver.find_elements(By.TAG_NAME, "address")
        self.rent_prices = self.driver.find_elements(By.PARTIAL_LINK_TEXT, "$")
        self.rent_links = self.driver.find_elements(By.CLASS_NAME, 'property-card-link')
        self.rent_links = [link.get_attribute("href") for link in self.rent_links]
        i = 0
        # Switching to pop up login window
        actions = ActionChains(self.driver).key_down(Keys.CONTROL).send_keys('n').key_up(Keys.CONTROL).perform()
        base_window = self.driver.window_handles[0]
        form_window = self.driver.window_handles[1]
        self.driver.switch_to.window(form_window)
        for element in self.rent_links:
            self.driver.get(FORM_URL)
            time.sleep(2)
            address = self.driver.find_element(By.XPATH, '/html/body/div/div[2]/form/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input')
            address.send_keys(self.rent_address[i].text)
            price = self.driver.find_element(By.XPATH, '/html/body/div/div[2]/form/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input')
            price.send_keys(self.rent_prices[i].text)
            link = self.driver.find_element(By.XPATH, '/html/body/div/div[2]/form/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input')
            link.send_keys(self.rent_links[i].text)
            send_button = self.driver.find_element(By.XPATH, '/html/body/div/div[2]/form/div[2]/div/div[3]/div[1]/div[1]/div/span')
            send_button.click()
            time.sleep(2)
            i += 1


rent_search = RentingResearchBot()
rent_search.get_rent_results()

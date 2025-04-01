import time
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


GOOGLE_FILE_URL = "https://docs.google.com/forms/d/e/1FAIpQLSdSW_6EXdP_G8dGJMzxjhO0U9dzz5ptGCop5kk9BJFU1GuRNQ/viewform?usp=header"
ZILLOW = "https://appbrewery.github.io/Zillow-Clone/"

header = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36",
    "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8",
}

# BS4 scraping the links, prices, and addresses
response = requests.get(url=ZILLOW, headers=header)
zillow_page = response.text

soup = BeautifulSoup(zillow_page, "html.parser")

link_tags = soup.find_all(class_="property-card-link")
links = [link.get("href") for link in link_tags]

price_tags = soup.find_all(class_="PropertyCardWrapper__StyledPriceLine")
prices = [
    price.getText().split("$")[1].split("+")[0].split("/")[0].replace(",", "")
    for price in price_tags
]

address_tag = soup.find_all("address")
addresses = [address.get_text().replace("|", "").strip() for address in address_tag]

# Selenium to fill the data in the questionnaire
edge_option = webdriver.EdgeOptions()
edge_option.add_experimental_option(name="detach", value=True)
driver = webdriver.Edge(options=edge_option)

driver.get(url=GOOGLE_FILE_URL)

for i in range(len(links)):
    address_answer = driver.find_element(
        By.XPATH,
        value='//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input',
    )
    price_answer = driver.find_element(
        By.XPATH,
        value='//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input',
    )
    link_answer = driver.find_element(
        By.XPATH,
        value='//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input',
    )
    submit_button = driver.find_element(
        By.XPATH, value='//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div'
    )

    time.sleep(1)

    address_answer.send_keys(addresses[i])
    price_answer.send_keys(prices[i])
    link_answer.send_keys(links[i])
    submit_button.click()
    try:
        other_answer = WebDriverWait(driver=driver, timeout=5).until(
            EC.element_to_be_clickable(
                (By.XPATH, "/html/body/div[1]/div[2]/div[1]/div/div[4]/a")
            )
        )
        other_answer.click()
    except TimeoutError:
        raise TimeoutError("Element was not clickable within seconds.")

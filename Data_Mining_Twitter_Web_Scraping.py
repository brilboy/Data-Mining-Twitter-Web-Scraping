# # Install Libraries

import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from time import sleep

from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options


PATH = "C:/Users/Ahmad Jibril H/Downloads/msedgedriver.exe"
driver = webdriver.Edge(PATH)
driver.get("https://twitter.com/login")


# # Login Setup

# Username
sleep(3)
username = driver.find_element(By.XPATH, "//input[@name='text']")
username.send_keys("YOURUSERID")
next_button = driver.find_element(By.XPATH, "//span[contains(text(), 'Next')]")
next_button.click()

# Password
sleep(3)
password = driver.find_element(By.XPATH, "//input[@name='password']")
password.send_keys("YOURPASSWORD")
next_button = driver.find_element(By.XPATH, "//span[contains(text(), 'Log in')]")
next_button.click()


# # Data Scraping

# Delete Searchbar
search = driver.find_element(By.XPATH, "//input[@data-testid='SearchBox_Search_Input']")
search.send_keys(Keys.CONTROL + 'a', Keys.BACKSPACE)

# Search
keyword = "'bali' (travel OR tourist OR trip OR tour OR vacation OR dance OR photo OR landmark OR temple OR journey OR culture OR island OR beach) lang:en until:2022-08-17 since:2022-08-01"
sleep(4)
search = driver.find_element(By.XPATH, "//input[@data-testid='SearchBox_Search_Input']")
search.send_keys(keyword)
search.send_keys(Keys.ENTER)


# Latest Switch
latest = driver.find_element(By.XPATH, "//span[contains(text(), 'Latest')]")
latest.click()


scrape = []
limit = 10000

content = driver.find_elements(By.XPATH, "//article[@data-testid='tweet']")
while True:
    for tweet in content:
        date = tweet.find_element(By.XPATH, ".//time").get_attribute('datetime')
        user_username = tweet.find_element(By.XPATH, ".//div[@data-testid='User-Name']").text
        tweet_text = tweet.find_element(By.XPATH, ".//div[@data-testid='tweetText']").text
        
        data = [date, user_username, tweet_text]
        scrape.append(data)
        driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
        sleep(5)
        content = driver.find_elements(By.XPATH, "//article[@data-testid='tweet']")
    if tweet == limit:
        break


# # Data Saving

import pandas as pd

df = pd.DataFrame(scrape)
df.to_csv("en-10-ags-all.csv") #header = None, skiprows = 1, names = ['Date', 'Username', 'Tweet'])


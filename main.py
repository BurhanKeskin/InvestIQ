import time

from selenium import webdriver
from selenium.webdriver.common.by import By



symbol = input("Enter the symbol of the company : ")
short_ema = int(input("Enter the short term value : "))
long_ema = int(input("Enter the long term value : "))

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--start-maximized") # set chrome to full-size screen

# initialize the google chrome
driver = webdriver.Chrome(options = chrome_options)

# url of the page that stores historical data of company
url = f"https://finance.yahoo.com/quote/{symbol}/history"

# make a request to visit the given website link
driver.get(url)

# Set timeout
driver.implicitly_wait(3)

#find the place of title on the webpage by using its XPATH
company_title = driver.find_element(By.XPATH, '//*[@id="nimbus-app"]/section/section/section/article/section[1]/div[1]/div/section')

# scroll to this title
driver.execute_script("arguments[0].scrollIntoView(true);", company_title)

# then download it
download_data = driver.find_element(By.XPATH, '//*[@id="nimbus-app"]/section/section/section/article/div[1]/div[2]/div/a').click()

# set a timeout
time.sleep(3)

# close the browser
driver.quit()
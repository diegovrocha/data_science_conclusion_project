from selenium import webdriver
from selenium.webdriver.common.keys import Keys

# create a new Firefox session
# driver = webdriver.Firefox()
driver = webdriver.Chrome()
driver.implicitly_wait(30)
driver.maximize_window()

# Navigate to the application home page
driver.get("https://ca.indeed.com/?r=us")
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import chromedriver_binary

options = Options()
#options.add_argument('--headless')
driver = webdriver.Chrome(options=options)

driver.get("https://www.youtube.com/watch?v=X9zw0QF12Kc")

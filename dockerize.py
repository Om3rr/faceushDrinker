#docker run -it -v $(pwd):/usr/workspace joyzoursky/python-chromedriver:3.6-alpine3.7-selenium python sheker-kolshau
from selenium import webdriver
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--window-size=1420,1080')
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
driver = webdriver.Chrome(chrome_options=chrome_options)

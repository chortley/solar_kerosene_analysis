from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from bs4 import BeautifulSoup
import re
import pandas as pd
import numpy as nps

url = 'https://www.swiss.com/ch/en/homepage'

chrome_options = webdriver.ChromeOptions()
driver = webdriver.Chrome('chromedriver.exe')
driver.implicitly_wait(20)
driver.get(url)


import re
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from time import sleep
import pandas as pd
import datetime

# epoch timestamp: 1483228800
start_from = datetime.datetime(2017,1,1,8,0,0).strftime('%s') 

gafata = ['^GSPC', 'GOOG', 'AAPL', 'FB', 'AMZN', '0700.HK', 'BABA']
source_data_path = "/Users/data/"

chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
# 设置下载地址
prefs = {'profile.default_content_settings.popups': 0, 'download.default_directory': f'{source_data_path}'}
chrome_options.add_experimental_option('prefs', prefs)

driver = webdriver.Chrome('/Users/hantao/Documents/践行群内容/extract-python/chromedriver', options = chrome_options)

driver = webdriver.Chrome('/usr/local/bin/chromedriver', options = chrome_options)

# get all csv files
driver.get(f'https://finance.yahoo.com/quote/{gafata[0]}/history')
sleep(5)

download_link = driver.find_element_by_xpath("// a[. // span[text() = 'Download Data']]").get_attribute("href")
for symbol in gafata:
    period1_changed = re.sub(r'period1=(\d+)', 'period1=1483228800', download_link)
    # if interval=1d, then stocks from various global exchanges would not align to each other in terms of date.
    interval_changed = re.sub(r'interval=(.*)&', 'interval=1wk&', period1_changed)
    dataURL = re.sub(r'download\/.*\?', f'download/{symbol}?', interval_changed)
    driver.get(dataURL)
    # 避免文件还没生成就解析文件
    sleep(5)


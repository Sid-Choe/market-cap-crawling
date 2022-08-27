import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import csv

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)

url = "https://finance.naver.com/sise/sise_market_sum.naver"

browser = webdriver.Chrome(service=Service(
    ChromeDriverManager().install()), options=chrome_options)

browser.get(url)
browser.maximize_window()
checkboxes = browser.find_elements(By.NAME, "fieldIds")

for box in checkboxes:
    if box.is_selected():
        box.click()

items_to_select = ["영업이익", "자산총계", "매출액"]

for box in checkboxes:
    parent = box.find_element(By.XPATH, "..")
    label = parent.find_element(By.TAG_NAME, "label").text
    if label in items_to_select:
        box.click()

btn_apply = browser.find_element(
    By.XPATH, '//a[@href="javascript:fieldSubmit()"]')
btn_apply.click()

df = pd.read_html(browser.page_source)[1]
df.dropna(axis="index", how="all", inplace="true")
df.dropna(axis="colums", how="all", inplace="true")

browser.quit()

from time import sleep

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

driver = webdriver.Firefox(executable_path="./geckodriver")
driver.get("https://en.wikipedia.org/wiki/List_of_countries_and_dependencies_by_population")
tbl = driver.find_element_by_class_name("wikitable")
countries = {}
for row in tbl.find_elements_by_tag_name('tr'):
    data = row.find_elements_by_tag_name("td")
    counts = len(data)
    if counts <= 0:
        continue
    data = data[0]
    a = data.find_element_by_tag_name('a')
    name = a.text
    countries[name] = a.get_attribute("href")

def get_pic(name, link):
    driver.get(link)
    cond = expected_conditions.visibility_of_all_elements_located((By.TAG_NAME, "body"))
    WebDriverWait(driver, 5).until(cond)
    card = driver.find_element_by_class_name("vcard")
    try:
        el = card.find_element_by_css_selector("tr > td > a > img").get_attribute("src")
    except Exception as x:
        el = card.find_element_by_css_selector("div.switcher-container > div > a.image > img").get_attribute("src")
    url = el.replace("/thumb", "").rsplit("/", 1)[0]
    with open("countriesp.txt", "a") as f:
        f.write((name + ":").ljust(20, " ") + url + "\n")

for k,v in countries.items():
    #print(k+" -> "+v)
    get_pic(k, v)

driver.quit()

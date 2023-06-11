from selenium import webdriver 
from selenium.webdriver.chrome.options import Options 
from selenium.webdriver.support.ui import WebDriverWait
import time

def current_location():
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'
    browser = webdriver.Chrome(r'C:\Users\jps_1\OneDrive\Desktop\Project_main\chromedriver.exe')
    timeout = 20
    browser.get("https://my-location.org/")
    wait = WebDriverWait(browser, timeout)
    time.sleep(4)
    elem=browser.find_element_by_xpath('//*[@id="latitude"]')
    latitude = elem.text
    elem = browser.find_element_by_xpath('//*[@id="longitude"]')
    longitude = elem.text
    map_link = 'http://maps.google.com/?q=' + latitude + ',' + longitude
    browser.close()
    return map_link

if __name__=="__main__":
    print(current_location())

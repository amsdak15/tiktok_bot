from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import pandas as pd

option = Options()
chrome_prefs = {}
option.experimental_options["prefs"] = chrome_prefs
chrome_prefs["profile.default_content_settings"] = { "popups": 1 }
option.add_argument('--disable-blink-features=AutomationControlled')
option.add_argument('disable-infobars')
option.add_experimental_option("useAutomationExtension", False)
option.add_experimental_option("excludeSwitches",["enable-automation"])
option.add_argument("--disable-extensions")
option.add_experimental_option("prefs", {
    "profile.default_content_setting_values.media_stream_mic": 1,
    "profile.default_content_setting_values.media_stream_camera": 1,
    "profile.default_content_setting_values.geolocation": 0,
    "profile.default_content_setting_values.notifications": 1
})
option.binary_location = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome' 
driver = webdriver.Chrome(options=option)

df = pd.read_excel('./tiktok.xlsx')

for i in range(len(df)):
    link= df['Link'][i]
    driver.get(link)
    driver.implicitly_wait(3)

    account_name = driver.find_element_by_xpath("//*[@id='main']/div[2]/div[2]/div/div/main/div/div[1]/span[1]/div/div[1]/div[1]/a[1]/h3").text
    df.loc[i,"Account"]= account_name

    description = driver.find_element_by_xpath("//*[@id='main']/div[2]/div[2]/div/div/main/div/div[1]/span[1]/div/div[1]/div[2]/strong").text
    df.loc[i,"Description"]= description

    like_count = driver.find_element_by_xpath("//*[@id='main']/div[2]/div[2]/div/div/main/div/div[1]/span[1]/div/div[1]/div[5]/div[2]/div[1]/strong").text
    df.loc[i,"Like"]= like_count

    comment_count = driver.find_element_by_xpath("//*[@id='main']/div[2]/div[2]/div/div/main/div/div[1]/span[1]/div/div[1]/div[5]/div[2]/div[2]/strong").text
    df.loc[i,"Comment"]= comment_count

    share_count = driver.find_element_by_xpath("//*[@id='main']/div[2]/div[2]/div/div/main/div/div[1]/span[1]/div/div[1]/div[5]/div[2]/div[3]/strong").text
    df.loc[i,"Share"]= share_count

    date = driver.find_element_by_xpath("//*[@id='main']/div[2]/div[2]/div/div/main/div/div[1]/span[1]/div/div[1]/div[1]/a[2]/h4").text
    df.loc[i,"Date"]= date

df.to_excel ('./tiktok.xlsx', index = False, header=True)

driver.close()

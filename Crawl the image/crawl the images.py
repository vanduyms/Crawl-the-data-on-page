from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.common.by import By
import urllib.request

# open browser and get url
driver = webdriver.Chrome('./chromedriver.exe')
driver.maximize_window()
driver.get('https://www.google.ca/imghp?hl=en&tab=ri&authuser=0&ogbl')

# search for image with the word "dog"
box = driver.find_element(by=By.XPATH, value='//*[@id="sbtc"]/div/div[2]/input')
box.send_keys('dog')
box.send_keys(Keys.ENTER)

# get the height of the webpage
last_height = driver.execute_script('return document.body.scrollHeight')

# scroll down the webpage
while True:
    driver.execute_script('window.scrollTo(0, document.body.scrollHeight)')
    time.sleep(2)
    new_height = driver.execute_script('return document.body.scrollHeight')

    # click on Show more the results
    try:
        driver.find_element(by=By.XPATH, value='//*[@id="islmp"]/div/div/div/div[1]/div[2]/div[2]/input').click()
        time.sleep(2)
    except:
        pass
    
    if new_height == last_height:
        break
    last_height = new_height

# download the images
for i in range(1, 100):
    try:
        img = driver.find_element(by=By.XPATH, value='//*[@id="islrg"]/div[1]/div['+str(i)+']/a[1]/div[1]/img')
        src = img.get_attribute('src')
        urllib.request.urlretrieve(src, './images/dog'+str(i)+'.png')
    except: 
        pass

# close the browser
driver.close()
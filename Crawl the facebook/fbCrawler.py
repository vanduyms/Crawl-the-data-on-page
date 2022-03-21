from base64 import decode
from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import string

options = webdriver.ChromeOptions()
options.add_argument("--disable-notifications")

driver = webdriver.Chrome(executable_path='./chromedriver.exe', chrome_options=options)
driver.maximize_window()

def login():
    driver.get("https://wwww.facebook.com/?_rdc=18_rdr")
    time.sleep(1)

    mail = driver.find_element_by_id("email")
    mail.send_keys('lanhthanhminh@gmail.com')
    time.sleep(1)

    pw = driver.find_element_by_id("pass")
    pw.send_keys('Duy6902')

    pw.send_keys(Keys.ENTER)
    time.sleep(7)

print('Scraper started !')
print('Logging in...')
login()
print('Logged in !')

file = open('searchPostUrl.txt', 'r')
lines = file.readlines()

count = 0
for line in lines:
    count += 1
    driver.get(line)
    time.sleep(7)

    post = driver.find_element_by_xpath("//div[@role='article' and @aria-posinset='1']")
    auth = post.find_element_by_tag_name('h2')

    fileName = 'Crawl '+str(count)+' .txt'
    with open(fileName, 'w', newline = '', encoding='utf8') as file:
        author = auth.text
        description = ''

        try:
            description = post.find_element_by_xpath(".//div[@data-ad-comet-preview='message' and @data-ad-preview='message']").text
        except:
            description = ''
        file.write('******************************************************\n')
        file.write('Author: '+ string.capwords(author) +'\n')
        file.write('Description: '+string.capwords(description)+'\n\n')

        while True:
            try:
                 driver.find_element_by_xpath("//span[contains(text(), 'View') and contains(text(), 'comment')]").click()
                 time.sleep(6)
            except:
                 break

        viewMore = post.find_elements_by_xpath(".//*[contains(text(), 'View') and contains(text(), 'more reply')]")
        for i in viewMore:
            try:
                i.click()
                time.sleep(1)
            except:
                pass   

        replies = post.find_elements_by_xpath(".//*[contains(text(), 'reply')] | .//*[contains(text(), 'replies')]")
        for node in replies:
            try:
                node.click()
                time.sleep(1)
            except:
                pass

        seeMore = driver.find_elements_by_xpath(".//*[contains(text(), 'See more')]")
        for node in seeMore:
            try:
                node.click()
                time.sleep(1)
            except:
                pass

        totalComments = driver.find_elements_by_xpath(".//div[@data-visualcompletion='ignore-dynamic']/div/div/ul/li//div[@role='article' and @tabindex='-1']")
        for comment in totalComments:
            commentBy = comment.find_element_by_xpath(".//span/span[@dir='auto']").text
            commentDescription = ""
            try:
                comments = comment.find_elements_by_xpath(".//div[@style='text-align: start;' and @dir='auto']")
                for cmt in comments:
                    commentDescription += ' ' + cmt.text
            except:
                commentDescription = ""
            file.write('Comment by: '+string.capwords(commentBy)+'\n')
            file.write('Comment: '+string.capwords(commentDescription)+'\n')

print ("Scraping Completed")

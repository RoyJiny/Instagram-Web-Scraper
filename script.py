from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import time

CHROME_DRIVER_PATH = "YOUR-CHROMEDRIVER-PATH"
USERNAME="YOUR-USERNAME"
PASSWORD="YOUR-PASSWORD"

# load chrome driver
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(CHROME_DRIVER_PATH,options=options)
driver.get("https://www.instagram.com/")

time.sleep(3)

# login
username_input = driver.find_element(by=By.NAME,value='username')
username_input.send_keys(USERNAME)
password_input = driver.find_element(by=By.NAME,value='password')
password_input.send_keys(PASSWORD)
password_input.send_keys(Keys.ENTER)

time.sleep(5)

# navigate to profile
profile_picture = driver.find_element(by=By.XPATH,value="//img[contains(@alt,'profile picture')]/parent::span")
profile_picture.click()
time.sleep(0.5)
profile_link = driver.find_element(by=By.XPATH,value="//div[text()='Profile']")
profile_link.click()

time.sleep(3)

# get followers
followers_link = driver.find_element(by=By.XPATH,value="//a[contains(@href,'/followers/')]")
followers_link.click()

time.sleep(3)

actions = ActionChains(driver)
actions.send_keys(Keys.TAB)
actions.send_keys(Keys.TAB)
actions.send_keys(Keys.END)
actions.perform()
time.sleep(1)
actions = ActionChains(driver)
actions.send_keys(Keys.TAB)
actions.send_keys(Keys.TAB)
actions.perform()

# adjust to more rounds if didnt go over all followers
for i in range(90):
    actions = ActionChains(driver)
    actions.send_keys(Keys.END)
    actions.perform()
    time.sleep(0.5)

followers = driver.find_elements(by=By.XPATH,value="//div[@aria-label='Followers']//ul//a")
followers_users = []
for follower in followers:
    followers_users.append(follower.get_attribute('href').split('https://www.instagram.com/')[1].replace('/',''))

followers_users = set(followers_users)
print(f"total of {len(followers_users)} followers")

# back to profile
actions = ActionChains(driver)
actions.send_keys(Keys.ESCAPE)
actions.perform()
time.sleep(1)

# get following
following_link = driver.find_element(by=By.XPATH,value="//a[contains(@href,'/following/')]")
following_link.click()

time.sleep(3)

actions = ActionChains(driver)
actions.send_keys(Keys.TAB)
actions.send_keys(Keys.TAB)
actions.send_keys(Keys.TAB)
actions.send_keys(Keys.TAB)
actions.send_keys(Keys.END)
actions.perform()
time.sleep(1)
actions = ActionChains(driver)
actions.send_keys(Keys.TAB)
actions.send_keys(Keys.TAB)
actions.send_keys(Keys.TAB)
actions.send_keys(Keys.TAB)
actions.perform()

# adjust to more rounds if didnt go over all following
for i in range(90):
    actions = ActionChains(driver)
    actions.send_keys(Keys.END)
    actions.perform()
    time.sleep(0.5)

following = driver.find_elements(by=By.XPATH,value="//div[@aria-label='Following']//ul//a")
following_users = []
for follower in following:
    following_users.append(follower.get_attribute('href').split('https://www.instagram.com/')[1].replace('/',''))

following_users = set(following_users)
print(f"total of {len(following_users)} following")


# start comparing
whitelist = set(open('./whitelist.txt','r').read().split(','))
print(f"ignoring {len(whitelist)} users from whitelist")
following_users = following_users - whitelist

for user in (following_users - followers_users):
    print(f"user {user} is not following back")

time.sleep(5)

driver.quit()
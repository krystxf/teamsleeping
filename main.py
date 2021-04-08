import os
import time
import json
from datetime import datetime
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


# pretty much self explanatory
load_dotenv()
# load meetings.json
with open('meetings.json') as f:
    meetings = json.load(f)

# settings from chromium
opt = Options()
opt.add_argument("--disable-infobars")
opt.add_argument("--disable-extensions")
# Pass the argument 1 to allow and 2 to block
opt.add_experimental_option("prefs", {
    "profile.default_content_setting_values.media_stream_mic": 1,
    "profile.default_content_setting_values.media_stream_camera": 1,
    "profile.default_content_setting_values.geolocation": 1,
    "profile.default_content_setting_values.notifications": 1
})
driver = webdriver.Chrome(options=opt)


def login():
    # go to login page
    driver.get("https://login.microsoftonline.com/81d89366-7747-4fe5-a737-97f57d0c18ec/oauth2/authorize?response_type=id_token&client_id=5e3ce6c0-2b1f-4285-8d4b-75ee78787346&redirect_uri=https%3A%2F%2Fteams.microsoft.com%2Fgo&state=a786692b-3205-4101-993e-748f9bec1714&&client-request-id=ac98faaf-f2e7-4a53-9a59-3fbb3f00cca2&x-client-SKU=Js&x-client-Ver=1.0.9&nonce=6a50e614-4c6f-4b53-ae10-7d7ea31b908b&domain_hint=")
    time.sleep(1)

    # fill email
    formInput = driver.find_element_by_xpath('//*[@id="i0116"]')
    formInput.send_keys(os.environ.get("EMAIL") + "\n")
    time.sleep(1)

    # fill password
    formInput = driver.find_element_by_xpath('//*[@id="i0118"]')
    formInput.send_keys(os.environ.get("PASSWORD") + "\n")
    time.sleep(1)

    # click remember password which actually doesnt work
    formInput = driver.find_element_by_xpath('//*[@id = "idSIButton9"]')
    formInput.click()
    time.sleep(10)


def connectToMeeting(meetingName, meetingUrl):

    # go to meting
    driver.get(meetingUrl)
    formInput = driver.find_element_by_xpath(
        '//*[@id = "buttonsbox"]/button[1]')
    formInput.click()
    time.sleep(5)

    # click connect
    formInput = driver.find_element_by_xpath(
        '//*[@id="page-content-wrapper"]/div[1]/div/calling-pre-join-screen/div/div/div[2]/div[1]/div[2]/div/div/section/div[1]/div/div/button')
    formInput.click()

    print("connected to " + meetingName)


login()

for x in range(len(meetings)):
    print("waiting for meeting")
    driver.get("https://product-image.juniqe-production.juniqe.com/media/catalog/product/seo-cache/x800/774/32/774-32-501P/Sweet-Dreams-Little-Flourishes-Aluminium-Print.jpg")
    while (meetings[x]["time"][:16] != str(datetime.now())[:16]):  # wait for meeting
        time.sleep(1)
    else:
        # connect to meeting
        connectToMeeting(meetings[x]["name"], meetings[x]["url"])
        # wait for meeting to end
        while (meetings[x]["time"][17:] != str(datetime.now())[11:16]):
            time.sleep(1)
        else:
            # disconnect from meeting
            print("disconnecting from meeting")

driver.delete_all_cookies()
driver.quit()
print("neplecha ukončena")

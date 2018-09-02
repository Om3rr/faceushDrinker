import os
import sys
import traceback
from selenium import webdriver
from croper import crop
from telegram import notify, sendPhoto, random_string
import json
from fullpage import fullpage_screenshot
import datetime
from time import sleep
from constants import *
from secrets import *
driver = None
def init_driver():
    global driver
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--window-size=1420,1080')
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(chrome_options=chrome_options)
    # driver.set_window_position(0, -2000)
def save_cookies():
    cookies = driver.get_cookies()
    with open('cookies.json', 'w+') as f:
        json.dump(cookies, f)


def check_login():
    driver.get('https://google.com')
    with open('cookies.json', 'r') as f:
        cookies = json.load(f)
        for cookie in cookies:
            driver.add_cookie(cookie)
    driver.get("https://www.facebook.com")
    try:
        text = driver.find_element_by_id("stream_pagelet").text
        save_cookies()
        return True
    except Exception as e:
        return False


def site_login():
    driver.get ("https://www.facebook.com")
    driver.find_element_by_id("email").send_keys(FB_EMAIL)
    driver.find_element_by_id("pass").send_keys(FB_PASSWORD)
    driver.find_element_by_xpath('//label[@id="loginbutton"]/input').click()
    save_cookies()

def wait_for_page_to_load():
    sleep(5)
    while True:
        if driver.execute_script('return document.readyState;') == 'complete':
            break
        else:
            sleep(1)


def search_in_group(group, search):
    driver.get(group)
    driver.find_element_by_xpath("//input[@aria-label='Search'][@placeholder='Search this group']").send_keys(search)
    driver.find_element_by_xpath('//button[@title="Search this group"][@type="submit"]').click()
    wait_for_page_to_load()
    try:
        driver.find_element_by_xpath("//a[contains(@href,'chronosort')]").click()
        wait_for_page_to_load()
    except Exception as e:
        pass

def get_items(chat_id=CHAT_ID):
    driver.set_window_size(1920, 1080)
    sleep(1)
    # document.evaluate('//div[starts-with(@id, "BrowseResultsContainer")]//div[starts-with(data-highlight-tokens,"[")]', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null)
    elements = driver.find_elements_by_xpath('//div[starts-with(@data-highlight-tokens,"[")]')
    screenshot_filename = f"captures/{random_string(10)}.png"
    fullpage_screenshot(driver, screenshot_filename)
    parsed = []
    for i,element in enumerate(elements):
        try:
            location = element.location
            size = element.size
            text = element.text
            description = text.split("\n")[4]
            timestamp = element.find_element_by_xpath("//a/abbr[@data-utime]")
            a_element = timestamp.find_element_by_xpath("..")
            href = a_element.get_attribute('href')
            time = str(datetime.datetime.now())
            path = f"captures/{random_string(12)}.png"
            crop(screenshot_filename, {'size': size, 'location': location}, path)
            parsed.append({'time': time, 'text': text, 'size': size, 'location': location, 'description': description, 'path': path, "href": href, "chat": chat_id})
        except Exception as e:
            print(e)
            traceback.print_tb(e.__traceback__)
            continue
    return parsed
import glob
import os
def empty_captures():
    files = glob.glob('captures/*')
    for f in files:
        os.remove(f)

def get_all_posts():
    with open('all_posts.json', 'rb') as f:
        all_posts = json.load(f)
        print(all_posts)
        all_descriptions = [x['description'] for x in all_posts]
    return all_descriptions, all_posts

def set_all_posts(all_posts):
    with open('all_posts.json', 'w+') as f:
        json.dump(all_posts, f)

def send_parsed(parsed, all_descriptions, all_posts):
    for parse in parsed:
        if parse['description'] in all_descriptions:
            continue
        all_posts.append(parse)
        msg_number = sendPhoto(parse)
        notify(parse, msg_number)
    return all_posts



def main():
    is_log_in = check_login()
    if not is_log_in:
        site_login()
    parsed = []
    for group in GROUPS:
        search = group['search']
        link = group['link']
        search_in_group(link, search)
        parsed += get_items(group['chat'])
    all_descriptions, all_posts = get_all_posts()
    before = len(all_posts)
    all_posts = send_parsed(parsed, all_descriptions, all_posts)
    after = len(all_posts)
    set_all_posts(all_posts)
    empty_captures()
    return after - before

def restart_program():
    os.execl(sys.executable, sys.executable, *sys.argv)
init_driver()
crashes = 0
while True:
    if crashes > 3:
        restart_program()
    try:
        print("Start Iter")
        main()
    except Exception as e:
        print("Boom")
        traceback.print_tb(e.__traceback__)
        print(e)
        crashes += 1
    sleep(3*60)

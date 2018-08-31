from selenium import webdriver
from croper import crop
from telegram import notify, sendPhoto, random_string
import json
from fullpage import fullpage_screenshot
import datetime
from time import sleep
from constants import *
driver = webdriver.Chrome()
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
    driver.find_element_by_id ("pass").send_keys(FB_PASSWORD)
    driver.find_element_by_xpath('//label[@id="loginbutton"]/input').click()
    save_cookies()

def wait_for_page_to_load():
    while True:
        if driver.execute_script('return document.readyState;') == 'complete':
            break
        else:
            sleep(1)


def search_in_group(group, search):
    driver.get(group)
    driver.find_element_by_xpath("//input[@aria-label='Search'][@placeholder='Search this group']").send_keys(search)
    driver.find_element_by_xpath('//button[@title="Search this group"][@type="submit"]').click()
    sleep(5)
    wait_for_page_to_load()
    try:
        driver.find_element_by_xpath("//a[contains(@href,'chronosort')]").click()
    except Exception as e:
        pass

def get_items():
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
            timestamp = element.find_element_by_class_name("timestamp")
            a_element = timestamp.find_element_by_xpath("..")
            href = a_element.get_attribute('href')
            time = str(datetime.datetime.now())
            path = f"captures/{random_string(12)}.png"
            crop(screenshot_filename, {'size': size, 'location': location}, path)
            parsed.append({'time': time, 'text': text, 'size': size, 'location': location, 'description': description, 'path': path, "href": href})
        except Exception as e:
            continue
    return parsed
import glob
import os
def empty_captures():
    files = glob.glob('captures/*')
    for f in files:
        os.remove(f)

def main():
    is_log_in = check_login()
    if not is_log_in:
        site_login()
    search_in_group(GROUP_LINK, SEARCH_FOR)
    parsed = get_items()
    with open('all_posts.json', 'rb') as f:
        all_posts = json.load(f)
        all_descriptions = [x['description'] for x in all_posts]
    for parse in parsed:
        if parse['description'] in all_descriptions:
            continue
        all_posts.append(parse)
        msg_number = sendPhoto(parse['path'], f"{parse['href']}")
        notify(parse['description'], msg_number)


    with open('all_posts.json', 'w+') as f:
        all_posts = json.dump(all_posts, f)

    empty_captures()


while True:
    print("Start")
    main()
    print("Finsish")
    sleep(60*3)

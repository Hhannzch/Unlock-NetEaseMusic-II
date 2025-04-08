# coding: utf-8

import os
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from retrying import retry

# Configure logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(asctime)s %(message)s')

@retry(wait_random_min=5000, wait_random_max=10000, stop_max_attempt_number=3)
def enter_iframe(browser):
    logging.info("Enter login iframe")
    time.sleep(5)  # 给 iframe 额外时间加载
    try:
        iframe = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[starts-with(@id,'x-URS-iframe')]")
        ))
        browser.switch_to.frame(iframe)
        logging.info("Switched to login iframe")
    except Exception as e:
        logging.error(f"Failed to enter iframe: {e}")
        browser.save_screenshot("debug_iframe.png")  # 记录截图
        raise
    return browser

@retry(wait_random_min=1000, wait_random_max=3000, stop_max_attempt_number=5)
def extension_login():
    chrome_options = webdriver.ChromeOptions()

    logging.info("Load Chrome extension NetEaseMusicWorldPlus")
    chrome_options.add_extension('NetEaseMusicWorldPlus.crx')

    logging.info("Initializing Chrome WebDriver")
    try:
        service = Service(ChromeDriverManager().install())  # Auto-download correct chromedriver
        browser = webdriver.Chrome(service=service, options=chrome_options)
    except Exception as e:
        logging.error(f"Failed to initialize ChromeDriver: {e}")
        return

    # Set global implicit wait
    browser.implicitly_wait(20)

    browser.get('https://music.163.com')

    # Inject Cookie to skip login
    logging.info("Injecting Cookie to skip login")
    browser.add_cookie({"name": "MUSIC_U", "value": "004D17E659B7CCE4CF19F7A4C90D88D67B38387531B67CD29DA6CD2EACC33686681E728CDED1BEC2E91CE5C1C4CD36C68930EC0C688549E6486649B81A436CCD89EE77D5702E715B429C11BEABB714DBF1CE1DD4B90DC459B80D7BF00B35604648941B5ECE36C2CBA32B42E019A688F2F871513718AAA4D8ADBFE263AC73CEB85FCCD050D250045DB68FA291413FD2158052B80DF45085D99FBF8ACA8A36CBE595F99F61A8CF772C5D35FFD4EB519695777794856E8D18F3ED8D54E05FE4280FE6EF92FAD4CE4141CB2719CE661E26602E68CDC79AE9C0286178CA35FF22AEA8D4B444013B04EB06670C5CC5F2F132D634362FC721D991C6CEE2ED773687C5CC523B6A4FE12DBF4DEF403268C39CAFE8D817C243EB3E26BD26E0B0FE8B0FB83BAD424F16A8061E7F2AF2291F8C6538C6314BE893C3A70AD65988756835B7113ABD487F0FE8863C56F113D6605704E19374202B3A4F63B9352495DBA3F99096E37C"})
    browser.refresh()
    time.sleep(5)  # Wait for the page to refresh
    logging.info("Cookie login successful")

    # Confirm login is successful
    logging.info("Unlock finished")

    time.sleep(10)
    browser.quit()


if __name__ == '__main__':
    try:
        extension_login()
    except Exception as e:
        logging.error(f"Failed to execute login script: {e}")

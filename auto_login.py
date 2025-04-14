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
    browser.add_cookie({"name": "MUSIC_U", "value": "00E3AA0655ABF6C977BA52DD2E1BECFD025EEF7BB327E353B0E5215A4E2E95EAA507DB4500A00CDE9D53B6A1D1F130800789BA77394E447C14A847354481065E2FB850C630C5B7A0DD535375209CFE7047F62D8B4EB2748F2DAD42B13373C9BF7BCC48BEB7FE031B0936529A12FB43527262670485ED3C0330F951D98515661593EC8330C4AC2BCEA9A6C0B0CA40B8650A2925A326F2361133A3DB6043760635EBC6CA61FCFE43CC5ACB67AB6AD4A18A02400AF2887C81DAFF09E70079689DFD8A22D3511E40B013B42690612387858E14CFB66C8E8F78DFAF4C534B60F386B1A76538B4136F6C017EFD9822B34F1BF2D6F929FA63DB89ACCD9F5B45DF2F123118EA7CD0DEE6D2238038CF0148A344572600FEBA857DEE3610B19A84E7ECD770E165BC724204C52AE87D7C33B3D5C9C78491EDE29A81C1CDEF03BBB4479ACB81B3336D2DB04539749E333769B9663EDB2637F2D17C0FD7D59F79E81938FE21D080"})
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

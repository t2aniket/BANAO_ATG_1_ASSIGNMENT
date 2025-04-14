import requests
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import logging


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    force=True,
    handlers=[
        logging.FileHandler("test_logs.txt", mode="w"), 
        logging.StreamHandler()
    ]
)

logger = logging.getLogger()


URL = "https://atg.party"
EMAIL = "t2aniketnaik@gmail.com"
PASSWORD = "International@123"
COVER_PHOTO_PATH = "/home/aniket/Desktop/icon-4399701_1280.jpg"
USERNAME = "t2anikeeet"
BIO = "Hi My Name is Aniket and I am an Automation Test Engineer"


def setup_driver():
    driver = webdriver.Chrome()
    driver.implicitly_wait(10)
    driver.maximize_window()
    return driver


def login(driver, wait):
    start_time=time.time()
    driver.get(URL)
    end_time=time.time()
    load_time=end_time-start_time
    logging.info(f"page load time is {load_time:.2f} seconds")
    login_btn = driver.find_element(By.XPATH, "//button[@class='atg-secondarybtn-tiny outer-header__loginbtn loginbtn_new']")
    login_btn.click()
    logging.info("Clicked LOGIN button")

    time.sleep(2)

    email = wait.until(EC.presence_of_element_located((By.ID, "email_landing")))
    email.send_keys(EMAIL)
    logging.info("Entered email")

    driver.find_element(By.ID, "password_landing").send_keys(PASSWORD)
    logging.info("Entered password")

    sign_in_btn = driver.find_element(By.XPATH, "//button[contains(text(), 'Sign In')]")
    sign_in_btn.click()
    logging.info("Clicked Sign In button")

    time.sleep(2)


def update_profile(driver, wait):
    driver.get("https://atg.party/edit-user-bio")

    username_edit_field = wait.until(EC.element_to_be_clickable((By.ID, "new_user_name")))
    bio_field = driver.find_element(By.ID, "about_me")
    cover_photo_btn = driver.find_element(By.ID, "upload_cover_img")
    cover_photo_upload = driver.find_element(By.ID, "upload1")
    cover_photo_savebtn = driver.find_element(By.ID, "profile_submit1")
    profile_save_btn = driver.find_element(By.XPATH, "//button[@class='acc-save atg-primarybtn-tiny']")

    username_edit_field.send_keys(USERNAME)
    logging.info("Username Entered")
    bio_field.send_keys(BIO)
    logging.info("Bio entered")

    cover_photo_btn.click()
    cover_photo_upload.send_keys(COVER_PHOTO_PATH)
    cover_photo_savebtn.click()
    time.sleep(3)
    status_text = driver.find_element(By.XPATH, "//div[@id='progress-wrp1']/div[@class='status']").get_attribute('textContent')
    wait.until(EC.text_to_be_present_in_element_attribute((By.XPATH, "//div[@id='progress-wrp1']/div[@class='status']"),"textContent", "100%"))
    logging.info("Photo uploaded")

    cover_pic_close_btn = driver.find_elements(By.XPATH, "//button[@class='btn-close']")
    cover_pic_close_btn[1].click()
    time.sleep(2)

    driver.execute_script("arguments[0].click();", profile_save_btn)
    logging.info("Profile saved")


def main():
    logger.info('Starting automation script')
    response = requests.get(URL)
    status_code = response.status_code

    if status_code == 200:
        logging.info(f"HTTP Response Code for {URL}: {status_code}")
        driver = setup_driver()
        wait = WebDriverWait(driver, 10)
        try:
            login(driver, wait)
            update_profile(driver, wait)
        except Exception as e:
            logging.error("An error occurred")
        finally:
            time.sleep(10)
            driver.quit()
    else:
        logging.error(f"HTTP Response Code for {URL}: {status_code}")
        exit()

if __name__ == "__main__":
    main()
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


def initialize_driver():
    driver = webdriver.Chrome()
    driver.maximize_window()
    return driver

def login_to_site(driver, username, password):
    driver.get("https://dictionary.cambridge.org/dictionary/")
    time.sleep(3)
    
    login_button = driver.find_element(By.XPATH, "//form[@id='gigya-login-form']/div[2]/div[3]/div/input")
    login_button.click()
    
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//input[@aria-label='Email']"))).send_keys(username)
    driver.find_element(By.XPATH, "//input[@name='password' and @aria-label='Password']").send_keys(password)

    driver.find_element((By.XPATH, "//input[@value='Log in']")).click()

def choose_dictionary(driver):
    dictionary_link = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//a[@href='https://dictionary.cambridge.org/dictionary/']"))
    )
    dictionary_link.click()
    english_option = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//a[@href='https://dictionary.cambridge.org/dictionary/english/']"))
    )
    english_option.click()

def search_for_word(driver, word):
    search_box = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "searchword"))
    )
    search_box.clear()
    search_box.send_keys(word)
    search_box.send_keys(Keys.RETURN)

def add_word_to_list(driver):
    add_to_list_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CLASS_NAME, "//button[text()='Add to list']"))
    )
    add_to_list_button.click()
    
    word_input_box = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "list-input-box"))
    )
    word_input_box.send_keys("Your Word")
    check_button = driver.find_element(By.XPATH, "//button[text()='Check']")
    check_button.click()

def close_driver(driver):
    driver.quit()

if __name__ == "__main__":
    username = "your_username"
    password = "your_password"
    words_to_add = ["example", "automation", "selenium"]
    driver = initialize_driver()
    
    try:
        login_to_site(driver, username, password)
        navigate_to_english_page(driver)
        
        for word in words_to_add:
            search_for_word(driver, word)
            add_word_to_list(driver)
            time.sleep(2) 
    finally:
        close_driver(driver)
# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


from selenium.common.exceptions import TimeoutException
import os

# xboard_index_html = "file:///mnt/g/crio.do/userrepo/suhaib0900-me_buildout_xboard/index.html"
xboard_index_html = "file://" + os.getenv("HTML_FILEPATH")

def get_first_accordian_class(browser):
    # FIXME - We need to add detailed logging so that users can get whats happening behind the scenes.
    btn, div_id = find_fist_accordian_btn_and_div(browser)
    print(div_id)
    btn.click()
    WebDriverWait(browser, 10).until(
        EC.visibility_of_element_located((By.ID, div_id)))
    print("wait until at least 30 cards are loaded")
    WebDriverWait(browser, 10).until(
        lambda wd: len(wd.find_elements(By.CLASS_NAME, 'card')) > 30
    )
    ref_div = browser.find_element_by_id(div_id)
    print(ref_div.get_attribute("class"))
    return ref_div.get_attribute("class")


def find_fist_accordian_btn_and_div(browser):
    browser.get(xboard_index_html)
    try:
        WebDriverWait(browser, 10).until(lambda driver: len(driver.find_elements_by_xpath(
            '//div[contains(@class, "card")]')) > 30)
    except:
        print("\n\nLogs in browser")
        for entry in browser.get_log("browser"):
            print(entry)

    element = browser.find_elements(By.TAG_NAME, "html")[0]
    print("\n\nPageHTML\n")
    print(element.get_attribute('innerHTML'))
    elements = browser.find_elements_by_xpath('//button')
    btn = elements[0]
    div_name = btn.get_attribute("data-target")
    return btn, div_name[1:]

def find_all_accordian_btns(browser):
    load_xboard_page_and_wait(browser)
    buttons = browser.find_elements_by_xpath('//button')
    return buttons, list(map(lambda btn: btn.get_attribute("data-target")[1:], buttons))


def load_xboard_page_and_wait(browser):
    browser.get(xboard_index_html)
    # WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'btn')))
    print("wait until at least 30 cards are loaded")
    try:
        WebDriverWait(browser, 10).until(
            lambda wd: len(wd.find_elements(By.CLASS_NAME, 'card')) > 30)
    except:
        print("\n\nLogs in browser")
        for entry in browser.get_log("browser"):
            print(entry)
    element = browser.find_elements(By.TAG_NAME, "html")[0]
    print("\n\nPageHTML\n")
    print(element.get_attribute('innerHTML'))


def get_courosal_element_ids(div_name):
    carousel_next_id = '//*[@id="' + div_name + '"]//*[starts-with(@class,"carousel-control-next")]'
    carousel_active_item = '//*[@id="' + div_name + '"]//div[@class="carousel-item active"]'
    return carousel_next_id, carousel_active_item





import time
import unittest
from unittest import TestCase

from selenium.webdriver import DesiredCapabilities

from test_helper import get_first_accordian_class, find_fist_accordian_btn_and_div, \
    get_courosal_element_ids, find_all_accordian_btns, load_xboard_page_and_wait
from functools import reduce
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

class Test_Main(TestCase):
    def get_web_driver(self):
        options = Options()
        options.add_argument("headless")
        options.add_argument("disable-infobars")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-web-security")
        options.add_argument("--no-sandbox")

        d = DesiredCapabilities.CHROME
        d['loggingPrefs'] = {'browser': 'ALL'}

        webdriver_chrome = webdriver.Chrome(options=options, desired_capabilities=d)
        return webdriver_chrome

    def test_first_carousel(self):
        print("###########test_first_carousel##############")
        driver = self.get_web_driver()
        btn, accordian_div = find_fist_accordian_btn_and_div(driver)
        next_element_path, active_element_path = get_courosal_element_ids(accordian_div)
        print("accordian button " + btn.text)
        print("next button inside active carousel " + next_element_path)
        print("root element in active carousel (ref#1)" + active_element_path)
        active_element = driver.find_element_by_xpath(active_element_path)
        next_element = driver.find_element_by_xpath(next_element_path)
        active_element_id = active_element.get_attribute("id")
        next_element.click()
        print("clicked on next button, now waiting for next carousel item to load" + next_element_path)
        time.sleep(3)
        next_id, current_active_element = get_courosal_element_ids(accordian_div)
        current_active_element = driver.find_element_by_xpath(current_active_element)
        print("active element after clicking on next button (ref#1)" + current_active_element.get_attribute("id"))
        print("ref#1 and ref#2 should not be same")
        self.assertNotEqual(active_element.get_attribute('innerHTML'), current_active_element.get_attribute('innerHTML'))


    def test_accordian(self):
        print("###########test_accordian##############")
        accordian_class = get_first_accordian_class(self.get_web_driver())
        print("Check if first accordian is expanded when the page loads")
        if not ("collapsing" in accordian_class or "show" in accordian_class) :
            self.fail("One of the class collapsing or show was expected in the accordian classes")

    def test_accordian_exists(self):
        print("###########test_accordian_exists##############")
        driver = self.get_web_driver()
        btn, accordian_div = find_fist_accordian_btn_and_div(driver)
        print("check if the accordian button is visible and clickable")
        self.assertTrue(btn.is_displayed())

    def test_at_least_one_accordian_expanded_on_load(self):
        print("###########test_at_least_one_accordian_expanded_on_load##############")
        driver = self.get_web_driver()
        btns, accordian_divs = find_all_accordian_btns(driver)
        divs_visibility = list(map(lambda div_id: driver.find_element_by_id(div_id).is_displayed(),accordian_divs))
        for temp_div_id in accordian_divs:
            print("div id " + temp_div_id + " is-visible? " + str(driver.find_element_by_id(temp_div_id).is_displayed()))
        some_visible = reduce((lambda x, y: x or y), divs_visibility)
        self.assertTrue(some_visible)

    def test_only_three_accordians(self):
        print("###########test_only_three_accordians##############")
        driver = self.get_web_driver()
        btns, accordian_divs = find_all_accordian_btns(driver)
        print("ensure that there are only three accordian classes, not less, not more :)")
        self.assertEqual(len(accordian_divs), 3)

    def test_thirty_cards(self):
        print("###########test_thirty_cards##############")
        driver = self.get_web_driver()
        load_xboard_page_and_wait(driver)
        cards_xpath = '//div[contains(@class, "card")]'
        all_cards = driver.find_elements_by_xpath(cards_xpath)
        print("All card Ids:" )
        self.print_text_values(all_cards)
        print("number of cards in the html", len(all_cards))
        print("Three accordians * 10 catousel cards = Total 30 cards expected minimum")
        self.assertGreaterEqual(len(all_cards), 30)

    def test_one_href_related_to_gardian_covid_news(self):
        print("###########test_one_href_related_to_gardian_covid_news##############")
        driver = self.get_web_driver()
        load_xboard_page_and_wait(driver)
        hrefs_xpath = '//div[contains(@class, "card")]//a'
        all_hrefs = driver.find_elements_by_xpath(hrefs_xpath)
        print("All hrefs:" )
        self.print_text_values(all_hrefs)
        print("The list above should contain at least one href that contains " + "covid-hospital-cases")
        filtered_cards = list(filter(lambda href: "covid-hospital-cases" in href.get_attribute("href"), all_hrefs))
        print("number of filtered html links", len(filtered_cards))
        self.assertGreaterEqual(len(filtered_cards), 1)

    def print_text_values(self, elements):
        for element in elements:
            print (element.text)

    def test_mi_rcb_visible_on_first_load(self):
        print("###########test_mi_rcb_visible_on_first_load##############")
        driver = self.get_web_driver()
        load_xboard_page_and_wait(driver)
        cards_xpath = '//*[contains(@class, "card-text")]'
        all_cards = driver.find_elements_by_xpath(cards_xpath)
        print("All card text:")
        self.print_text_values(all_cards)
        print('''Above printed are card ids, out of which, there is one card related to Coronavirus. The text starts with ,
               "The number of coronavirus"
               The card that has this message should be visible on load''')
        filtered_cards = list(filter(lambda card_text : "The number of coronavirus" in card_text.text, all_cards))
        visible_cards = list(filter(lambda card_text : card_text.is_displayed(), all_cards))
        print("Visible card:")
        self.print_text_values(visible_cards)
        print("number of cards in the html", len(filtered_cards))
        self.assertGreaterEqual(len(filtered_cards), 1)
        self.assertTrue(filtered_cards[0].is_displayed())

    def test_quim_image_is_displayed_on_first_load(self):
        print("###########test_quim_image_is_displayed_on_first_load##############")
        img_src = 'https://cdn.flipboard.com/guim.co.uk/c018603dc3befcf6285482a0595ea756fa447fba/original.jpg'
        print("expected image location - " + img_src)
        driver = self.get_web_driver()
        load_xboard_page_and_wait(driver)
        imgs_xpath = '//div[contains(@class, "card")]//img'
        all_images = driver.find_elements_by_xpath(imgs_xpath)
        print('''Each card on the page will have an image, out of which, there is one image that points to ,
                       image location mentioned above, The card that has this message should be visible on load''')
        filtered_cards = list(filter(lambda card_img : img_src == card_img.get_attribute("src"), all_images))
        print("number of cards in the html", len(filtered_cards))
        self.assertGreaterEqual(len(filtered_cards), 1)
        self.assertTrue(filtered_cards[0].is_displayed())


if __name__ == '__main__':
    unittest.main()


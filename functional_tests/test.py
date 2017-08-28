# -*- coding: utf-8 -*-
# @Author: szhang
# @Date:   2017-08-09 00:31:30
# @Last Modified by:   Shaonan Zhang
# @Last Modified time: 2017-08-28 09:26:27
# tdd w/ python book first file
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest
from contextlib import contextmanager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import staleness_of


class NewVisitorTestCase(StaticLiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    @contextmanager
    def wait_for_page_load(self, timeout=30):
        old_page = self.browser.find_element_by_tag_name("html")
        yield WebDriverWait(self.browser, timeout).until(
            staleness_of(old_page)
        )

    def _check_for_row_in_list_table(self, row_text):
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        rows_text_list = [row.text for row in rows]
        self.assertIn(row_text, rows_text_list, "[{}] didn't appear in table".format(row_text))

    def _create_new_item(self, text):
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys(text)
        inputbox.send_keys(Keys.ENTER)

    def test_can_start_a_list_and_retrieve_it_later(self):
        # Edith has heard about a cool new online to-do app, she goes to check out its homepage.
        self.browser.get(self.live_server_url)

        # She notices the page title mentions 'To-Do'
        expected_title_keyword = 'To-Do'
        self.assertIn(expected_title_keyword, self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn(expected_title_keyword, header_text)

        # She was invited to create a to-do right away
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(inputbox.get_attribute('placeholder'), 'Enter a to-do item')

        # When she hits enter, the page updates, and now the page lists
        self._create_new_item('Buy peacock feathers')
        # "1: Buy peacock feathers" as an item in a to-do list
        with self.wait_for_page_load(timeout=10):
            edith_list_url = self.browser.current_url
            self.assertRegex(edith_list_url, r'/lists/\d+')
            self._check_for_row_in_list_table('1: Buy peacock feathers')

        # There is still a text box inviting her to add another item.
        # She enters "Use peacock feathers to make a fly"
        self._create_new_item('Use peacock feathers to make a fly')
        # The page updates again, and now shows both items on her list
        with self.wait_for_page_load(timeout=10):
            edith_list_url_second_post = self.browser.current_url
            self.assertEqual(edith_list_url_second_post, edith_list_url)
            self._check_for_row_in_list_table('1: Buy peacock feathers')
            self._check_for_row_in_list_table('2: Use peacock feathers to make a fly')

        # Now a new user, Francis, comes along to the site.
        # we use a new browser session to makes sure that no information of Edith
        # is comming through cookies etc
        self.browser.quit()
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)
        # Francis visits the page, found no information about Edith's list
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy peacock feathers', page_text)
        self.assertNotIn('make a fly', page_text)

        # Francis starts a new list by entering a new item
        self._create_new_item('Buy milk')

        with self.wait_for_page_load(timeout=10):
            # Francis gets his own URL
            francis_list_url = self.browser.current_url
            self.assertRegex(francis_list_url, r'/lists/\d+')
            self.assertNotEqual(francis_list_url, edith_list_url)

            # Again, there is no trace of Edith's list
            page_text = self.browser.find_element_by_tag_name('body').text
            self.assertNotIn('Buy peacock feathers', page_text)
            self._check_for_row_in_list_table('1: Buy milk')

    def test_layout_and_styling(self):
        # Edith goes to home page
        self.browser.get(self.live_server_url)
        self.browser.set_window_size(1024, 768)

        # She notices the input box is nicely centered
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertAlmostEqual(inputbox.location['x'] + inputbox.size['width'] / 2, 512, delta=5)
        # She starts a new list and sees the input is nicely
        # centered there too
        self._create_new_item('testing\n')
        with self.wait_for_page_load(timeout=10):
            inputbox = self.browser.find_element_by_id('id_new_item')
            self.assertAlmostEqual(inputbox.location['x'] + inputbox.size['width'] / 2, 512, delta=5)
        # Edith wonder whether the sites will remember her lists.
        # Then she see that the website has generated a unique url for her

        # She visits that URL, her to-do list is still there

        # Edith closes the browser


if __name__ == '__main__':
    unittest.main()

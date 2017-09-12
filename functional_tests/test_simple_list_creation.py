# -*- coding: utf-8 -*-
# @Author: szhang
# @Date:   2017-08-09 00:31:30
# @Last Modified by:   Shaonan Zhang
# @Last Modified time: 2017-08-30 21:24:56
# tdd w/ python book first file
import unittest
from selenium import webdriver
from .base import FunctionalTest


class NewVisitorTest(FunctionalTest):

    def test_can_start_a_list_and_retrieve_it_later(self):
        # Edith has heard about a cool new online to-do app, she goes to check out its homepage.
        self.browser.get(self.server_url)

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
        self.browser.get(self.server_url)
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


if __name__ == '__main__':
    unittest.main()

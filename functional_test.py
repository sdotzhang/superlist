# -*- coding: utf-8 -*-
# @Author: szhang
# @Date:   2017-08-09 00:31:30
# @Last Modified by:   Shaonan Zhang
# @Last Modified time: 2017-08-13 22:16:01
# tdd w/ python book first file

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest


class NewVisitorTestCase(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def test_can_start_a_list_and_retrieve_it_later(self):
        # Edith has heard about a cool new online to-do app, she goes to check out its homepage.
        self.browser.get('http://localhost:8000')

        # She notices the page title mentions 'To-Do'
        expected_title_keyword = 'To-Do'
        self.assertIn(expected_title_keyword, self.browser.title)
        header_text = self.browser.fing_element_by_tag_name('h1').text
        self.assertIn(expected_title_keyword, header_text)

        # She was invited to create a to-do right away
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(inputbox.get_attribute('placeholder'), 'Enter a to-do item')

        # She types 'Buy peacock feathers' into text input box
        inputbox.send_keys('Buy peacock feathers')

        # When she hits enter, the page updates, and now the page lists
        # "1: Buy peacock feathers" as an item in a to-do list
        inputbox.send_keys(Keys.ENTER)
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertTrue(any(row.text == '1: Buy peacock feathers' for row in rows))

        # There is still a text box inviting her to add another item.
        # She enters "Use peacock feathers to make a fly"

        # The page updates again, and now shows both items on her list

        # Edith wonder whether the sites will remember her lists.
        # Then she see that the website has generated a unique url for her

        # She visits that URL, her to-do list is still there

        # Edith closes the browser


if __name__ == '__main__':
    unittest.main()

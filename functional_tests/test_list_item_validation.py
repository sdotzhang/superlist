# -*- coding: utf-8 -*-
# @Author: szhang
# @Date:   2017-08-09 00:31:30
# @Last Modified by:   Shaonan Zhang
# @Last Modified time: 2017-08-30 21:24:56
# tdd w/ python book first file
import unittest
from .base import FunctionalTest

class ItemValidationTest(FunctionalTest):
    def test_cannot_add_empty_list_items(self):
        # Edith goes to the home page and accidentally tries to submit
        # an empty list item. She hits Enter on the empty input box
        self.browser.get(self.server_url)
        self._create_new_item('\n')

        # The home page refreshes, and there is an error message saying
        # that list items cannot be blank
        with self.wait_for_page_load(timeout=10):
            error = self.browser.find_element_by_css_selector('.has-error')
            self.assertEqual(error.text, "You can't create empty list items")

        # She tries again with some text for the item, which now works
        self._create_new_item('Buy milk\n')
        with self.wait_for_page_load(timeout=10):
            self._check_for_row_in_list_table('1: Buy milk')

        # Perversely, she now decides to submit a second blank list item
        self._create_new_item('\n')

        # She receives a similar warning on the list page
        with self.wait_for_page_load(timeout=10):
            error = self.browser.find_element_by_css_selector('.has-error')
            self.assertEqual(error.text, "You can't create empty list items")

        # And she can correct it by filling some text in
        self._create_new_item('Make tea\n')
        with self.wait_for_page_load(timeout=10):
            self._check_for_row_in_list_table('1: Buy milk')
            self._check_for_row_in_list_table('2: Make tea')


if __name__ == '__main__':
    unittest.main()

# -*- coding: utf-8 -*-
# @Author: szhang
# @Date:   2017-08-09 00:31:30
# @Last Modified by:   Shaonan Zhang
# @Last Modified time: 2017-08-30 21:24:56
# tdd w/ python book first file
import unittest
from .base import FunctionalTest


class LayoutAndStylingTest(FunctionalTest):
    def test_layout_and_styling(self):
        # Edith goes to home page
        self.browser.get(self.server_url)
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

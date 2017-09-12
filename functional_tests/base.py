# -*- coding: utf-8 -*-
# @Author: szhang
# @Date:   2017-08-09 00:31:30
# @Last Modified by:   Shaonan Zhang
# @Last Modified time: 2017-08-30 21:24:56
# tdd w/ python book first file
import sys
import unittest
from contextlib import contextmanager

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.expected_conditions import staleness_of
from selenium.webdriver.support.ui import WebDriverWait


class FunctionalTest(StaticLiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        for arg in sys.argv:
            if 'liveserver' in arg:
                cls.server_url = 'http://' + arg.split('=')[1]
                return
        super(FunctionalTest, cls).setUpClass()
        cls.server_url = cls.live_server_url

    @classmethod
    def tearDownClass(cls):
        if cls.server_url == cls.live_server_url:
            super(FunctionalTest, cls).tearDownClass()

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


if __name__ == '__main__':
    unittest.main()

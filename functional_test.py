# -*- coding: utf-8 -*-
# @Author: szhang
# @Date:   2017-08-09 00:31:30
# @Last Modified by:   szhang
# @Last Modified time: 2017-08-10 09:08:02
# tdd w/ python book first file

import logging
from selenium import webdriver

browser = webdriver.Firefox()

# Edith has heard about a cool new online to-do app, she goes to check out its homepage.
browser.get('http://localhost:8000')

# She notices the page title mentions 'To-Do'
expected_title_keyword = 'To-Do'
assert expected_title_keyword in browser.title, "Error asserting {} in title".format(expected_title_keyword)

# She was invited to create a to-do right away

# She types 'Buy peacock feathers' into text input box

# When she hits enter, the page updates, and now the page lists
# "1: Buy peacock feathers" as an item in a to-do list

# There is still a text box inviting her to add another item.
# She enters "Use peacock feathers to make a fly"

# The page updates again, and now shows both items on her list

# Edith wonder whether the sites will remember her lists.
# Then she see that the website has generated a unique url for her

# She visits that URL, her to-do list is still there

# Edith closes the browser
browser.close()

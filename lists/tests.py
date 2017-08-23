from django.test import TestCase
from django.core.urlresolvers import resolve
from django.http import HttpRequest
from django.template.loader import render_to_string

from lists.views import home_page
from lists.models import Item, TodoList


class HomePageTest(TestCase):

    def test_root_url_resolve_to_home_page_view(self):
        found = resolve('/')
        self.assertEqual(found.func, home_page)

    def test_home_page_return_correct_content(self):
        request = HttpRequest()
        response = home_page(request)
        expected_html = render_to_string('home.html')
        self.assertEqual(response.content.decode(), expected_html)


class ListAndItemModelTest(TestCase):

    def test_saving_and_retrieving_item(self):
        todo_list = TodoList()
        todo_list.save()

        first_item = Item()
        first_item.text = 'The first (ever) list item'
        first_item.todo_list = todo_list
        first_item.save()
        second_item = Item()
        second_item.text = 'Item the second'
        second_item.todo_list = todo_list
        second_item.save()

        saved_first_list = TodoList.objects.first()
        self.assertEqual(saved_first_list, todo_list)
        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.text, 'The first (ever) list item')
        self.assertEqual(first_saved_item.todo_list, todo_list)
        self.assertEqual(second_saved_item.text, 'Item the second')
        self.assertEqual(second_saved_item.todo_list, todo_list)


class ListViewTest(TestCase):

    def test_display_all_items(self):
        todo_list = TodoList.objects.create()
        Item.objects.create(text='itemey 1', todo_list=todo_list)
        Item.objects.create(text='itemey 2', todo_list=todo_list)
        response = self.client.get('/lists/uniq_url/')
        self.assertContains(response, 'itemey 1')
        self.assertContains(response, 'itemey 2')

    def test_uses_list_templates(self):
        response = self.client.get('/lists/uniq_url/')
        self.assertTemplateUsed(response, 'list.html')


class NewListTest(TestCase):

    def test_saving_a_POST_request(self):
        new_item_text = 'A new list item'
        self.client.post('/lists/new', data={'item_text': new_item_text})
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, new_item_text)

    def test_redirects_after_POST(self):
        response = self.client.post('/lists/new', data={'item_text': 'A new list item'})
        self.assertRedirects(response, '/lists/uniq_url/')

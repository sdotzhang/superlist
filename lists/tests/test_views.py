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


class ListViewTest(TestCase):

    def test_displays_only_items_for_that_list(self):
        correct_todo_list = TodoList.objects.create()
        Item.objects.create(text='itemey 1', todo_list=correct_todo_list)
        Item.objects.create(text='itemey 2', todo_list=correct_todo_list)
        response = self.client.get('/lists/{}/'.format(correct_todo_list.id))
        other_todo_list = TodoList.objects.create()
        Item.objects.create(text='other list item 1', todo_list=other_todo_list)
        Item.objects.create(text='other list item 2', todo_list=other_todo_list)
        self.assertContains(response, 'itemey 1')
        self.assertContains(response, 'itemey 2')
        self.assertNotContains(response, 'other list item 1')
        self.assertNotContains(response, 'other list item 2')

    def test_uses_list_templates(self):
        temp_todo_list = TodoList.objects.create()
        response = self.client.get('/lists/{}/'.format(temp_todo_list.id))
        self.assertTemplateUsed(response, 'list.html')

    def test_passes_correct_list_template(self):
        correct_todo_list = TodoList.objects.create()
        TodoList.objects.create()
        response = self.client.get('/lists/{}/'.format(correct_todo_list.id))
        self.assertEqual(response.context['todo_list'], correct_todo_list)

class NewListTest(TestCase):

    def test_saving_a_POST_request(self):
        new_item_text = 'A new list item'
        self.client.post('/lists/new', data={'item_text': new_item_text})
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        new_todolist = TodoList.objects.first()
        self.assertEqual(new_item.text, new_item_text)
        self.assertEqual(new_item.todo_list.id, new_todolist.id)

    def test_save_a_POST_request_to_an_existing_list(self):
        correct_todo_list = TodoList.objects.create()
        TodoList.objects.create()
        self.assertEqual(TodoList.objects.count(), 2)
        new_item_text = 'A new list item'
        self.client.post('/lists/{}/add_item'.format(correct_todo_list.id), data={'item_text': new_item_text})
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, new_item_text)
        self.assertEqual(new_item.todo_list, correct_todo_list)

    def test_redirects_after_POST(self):
        correct_todo_list = TodoList.objects.create()
        TodoList.objects.create()
        response = self.client.post('/lists/{}/add_item'.format(correct_todo_list.id), data={'item_text': 'A new list item'})
        self.assertRedirects(response, '/lists/{}/'.format(correct_todo_list.id))

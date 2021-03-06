from django.core.exceptions import ValidationError
from django.test import TestCase
from lists.models import Item, TodoList


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

    def test_cannot_save_empty_list(self):
        todo_list = TodoList.objects.create()
        item = Item(todo_list=todo_list, text="")
        with self.assertRaises(ValidationError):
            item.save()
            item.full_clean()

    def test_get_absolute_url(self):
        todo_list = TodoList.objects.create()
        self.assertEqual(todo_list.get_absolute_url(), '/lists/{}/'.format(todo_list.id))

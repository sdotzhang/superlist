from django.db import models
from django.core.urlresolvers import reverse


class TodoList(models.Model):

    def get_absolute_url(self):
        return reverse('view_list', args=[self.id])


class Item(models.Model):
    text = models.TextField(default='')
    todo_list = models.ForeignKey(TodoList, default=None)


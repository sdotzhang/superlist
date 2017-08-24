from django.shortcuts import render, redirect
from lists.models import Item, TodoList

# Create your views here.
def home_page(request):
    return render(request, 'home.html')

def view_list(request, todo_list_id):
    todo_list = TodoList.objects.get(id=todo_list_id)
    return render(request, 'list.html', {'todo_list': todo_list})

def new_list(request):
    todo_list = TodoList.objects.create()
    Item.objects.create(text=request.POST['item_text'], todo_list=todo_list)
    return redirect('/lists/{}/'.format(todo_list.id))

def add_item(request, todo_list_id):
    todo_list = TodoList.objects.get(id=todo_list_id)
    Item.objects.create(text=request.POST['item_text'], todo_list=todo_list)
    return redirect('/lists/{}/'.format(todo_list.id))

from django.shortcuts import render, redirect
from lists.models import Item, TodoList

# Create your views here.
def home_page(request):
    return render(request, 'home.html')

def view_list(request):
    items = Item.objects.all()
    return render(request, 'list.html', {'items': items})

def new_list(request):
    todo_list = TodoList.objects.create()
    Item.objects.create(text=request.POST['item_text'], todo_list=todo_list)
    return redirect('/lists/uniq_url/')

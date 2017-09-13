from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect
from lists.models import Item, TodoList

# Create your views here.
def home_page(request):
    return render(request, 'home.html')

def view_list(request, todo_list_id):
    todo_list = TodoList.objects.get(id=todo_list_id)
    if request.method == 'POST':
        item = Item.objects.create(text=request.POST['item_text'], todo_list=todo_list)
        try:
            item.full_clean()
            item.save()
            return redirect(todo_list)
        except ValidationError:
            error = "You can't create empty list items"
            item.delete()
            return render(request, 'list.html', {'todo_list': todo_list, 'error': error})
    return render(request, 'list.html', {'todo_list': todo_list})

def new_list(request):
    todo_list = TodoList.objects.create()
    item = Item.objects.create(text=request.POST['item_text'], todo_list=todo_list)
    try:
        item.full_clean()
        item.save()
    except ValidationError:
        todo_list.delete()
        item.delete()
        error = "You can't create empty list items"
        return render(request, 'home.html', {'error': error})
    return redirect(todo_list)

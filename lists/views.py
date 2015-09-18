from django.shortcuts import redirect, render
from lists.models import Item, List

def home_page(request):
	count_list = Item.objects.count()

	comment = ""
	if count_list == 0:
		comment = "Yey, waktunya berlibur"
	elif count_list < 5:
		comment = "Sibuk tapi santai"
	else:
		comment = "Oh tidak"

	return render(request, 'home.html', {'comment': comment})

def view_list(request):
	items = Item.objects.all()

	return render(request, 'list.html', {'items': items})

def new_list(request):
	list_ = List.objects.create()
	Item.objects.create(text=request.POST['item_text'], list=list_)
	return redirect('/lists/the-only-list-in-the-world/')
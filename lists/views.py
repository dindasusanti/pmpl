from django.shortcuts import redirect, render
from lists.models import Item, List

def home_page(request):
	comment = "Yey, waktunya berlibur"
	return render(request, 'home.html', {'comment': comment})

def new_list(request):
	list_ = List.objects.create()
	Item.objects.create(text=request.POST['item_text'], list=list_)
	return redirect('/lists/%d/' % (list_.id,))

def add_item(request, list_id):
	list_ = List.objects.get(id=list_id)
	Item.objects.create(text=request.POST['item_text'], list=list_)
	return redirect('/lists/%d/' % (list_.id,))

def view_list(request, list_id):
	list_ = List.objects.get(id=list_id)
	count_list = Item.objects.filter(list_id=list_id).count()

	comment = ""
	if count_list == 0:
		comment = "Yey, waktunya berlibur"
	elif count_list < 5:
		comment = "Sibuk tapi santai"
	else:
		comment = "Oh tidak"
	return render(request, 'list.html', {'list': list_, 'comment': comment})
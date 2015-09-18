from django.shortcuts import redirect, render
from lists.models import Item

def home_page(request):
	if request.method == 'POST':
		Item.objects.create(text=request.POST['item_text'])
		return redirect('/')
	
	items = Item.objects.all()
	count_list = Item.objects.count()
	comment = ""
	if count_list == 0:
		comment = "Yey, waktunya berlibur"
	elif count_list < 5:
		comment = "Sibuk tapi santai"
	else:
		comment = "Oh tidak"
	return render(request, 'home.html', {'items': items, 'comment': comment})

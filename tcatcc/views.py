from django.shortcuts import render
from django.http import HttpResponse

from .models import Item
from .forms import createItemForm

# Create your views here.
def index(request):
	itemlist = Item.objects.all()
	context = {
		'items': itemlist,
	}
	return render(request,'tcatcc/index.html',context)

def newItemView(request):
	form = createItemForm()
	if request.method == "POST":
		form = createItemForm(request.POST)
		if form.is_valid():
			newItem = Item()
			newItem.name = form.get_cleaned_data['name']
			newItem.description = form.get_cleaned_data['description']

			newItem.owner = request.user

			newItem.threshold = form.get_cleaned_data['threshold']
			newItem.expiryDate = form.get_cleaned_data['expiryDate']

			newItem.save()

	context = {
		'form': form,
	}

	return render(request,'tcatcc/item_create.html',context)
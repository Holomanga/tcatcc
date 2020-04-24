from django.shortcuts import render, HttpResponseRedirect
from django.http import HttpResponse
from django.urls import reverse

from .models import Item
from .forms import createItemForm

# Create your views here.
def index(request):
	itemlist = Item.objects.filter(stillOpen=True)
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
			newItem.name = form.cleaned_data['name']
			newItem.description = form.cleaned_data['description']

			newItem.owner = request.user

			newItem.threshold = form.cleaned_data['threshold']
			newItem.expiryDate = form.cleaned_data['expiryDate']

			newItem.save()
			return HttpResponseRedirect(reverse('tcatcc:index') )

	context = {
		'form': form,
	}

	return render(request,'tcatcc/item_create.html',context)
from django.shortcuts import render, HttpResponseRedirect, get_object_or_404
from django.http import HttpResponse
from django.urls import reverse
from django.utils import timezone

from django.contrib.auth import authenticate, login

from .models import Item, AgreementRequest
from .forms import createItemForm, subscribeForm, customUserCreationForm

# Create your views here.
def index(request):
	itemlist = Item.objects.exclude(expiryDate__lt=timezone.now()).filter(stillOpen=True)
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

			if request.user.is_authenticated:
				newItem.owner = request.user

			newItem.threshold = form.cleaned_data['threshold']
			newItem.expiryDate = form.cleaned_data['expiryDate']

			newItem.save()
			return HttpResponseRedirect(reverse('tcatcc:index'))

	context = {
		'form': form,
	}

	return render(request,'tcatcc/item_create.html',context)

def detailItemView(request, itemid):
	item = get_object_or_404(Item,pk=itemid)
	sForm = subscribeForm()
	if request.user.is_authenticated:
		sForm.fields['email'].initial = request.user.email

	if request.method == "POST":
		sForm = subscribeForm(request.POST)
		if sForm.is_valid():
			newCommitment = AgreementRequest()
			newCommitment.item = item
			newCommitment.email = sForm.cleaned_data['email']
			newCommitment.save()

			#should actually just send you the validation email
			#and that view creates your new subscription
			return HttpResponseRedirect(reverse('tcatcc:index'))

	context = {
		'item': item,
		'subscribeForm': sForm,
	}

	return render(request,'tcatcc/item_detail.html',context)

def confirmSignupView(request, uuid):
	signup = get_object_or_404(AgreementRequest,pk=uuid)
	signup.validate()
	return HttpResponseRedirect(reverse('tcatcc:index'))

def signUp(request):
	form = customUserCreationForm()
	if request.method == "POST":
		form = customUserCreationForm(request.POST)
		if form.is_valid():
			username = form.cleaned_data['username']
			raw_password = form.cleaned_data['password1']
			email = form.cleaned_data['email']
			form.save()
			user = authenticate(username=username, password=raw_password)
			login(request, user)
			return HttpResponseRedirect(reverse('markets:index'))

	context = {
		'form':form,
	}
	
	return render(request, 'registration/sign_up.html', context)
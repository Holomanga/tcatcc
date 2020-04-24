from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
import html5.forms.widgets as html5_widgets

from .models import Item

class createItemForm(forms.ModelForm):
	class Meta:
		model = Item
		fields = ['name', 'description', 'threshold', 'expiryDate']
		labels = {
			'expiryDate': _('Expiry Date')
		}

	def __init__(self,*args,**kwargs):
		super().__init__(*args,**kwargs)
		self.fields['expiryDate'].widget = html5_widgets.DateInput()

	def clean_threshold(self):
		data = self.cleaned_data['threshold']
		if data <= 0:
			raise ValidationError(_('Threshold must be positive.'))
		return data

	def clean_expiryDate(self):
		data = self.cleaned_data['expiryDate']
		if data is not None:
			if data <= timezone.now():
				raise ValidationError(_('Expiry date must be in the future if present.'))
		return data

from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class customUserCreationForm(UserCreationForm):
	class Meta(UserCreationForm.Meta):
		model = User
		fields = UserCreationForm.Meta.fields# + ('email',)
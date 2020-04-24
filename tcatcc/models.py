from django.db import models
from django.utils import timezone

from django.contrib.auth.models import User

from django.core.mail import send_mail

# Create your models here.
class Item(models.Model):
	name = models.TextField()
	description = models.TextField()
	owner = models.ForeignKey(User, on_delete=models.CASCADE)

	threshold = models.IntegerField()
	expiryDate =  models.DateTimeField(blank=True,null=True)

	stillOpen = models.BooleanField(default=True)

	def __str__(self):
		return self.name

	def agreers(self):
		return self.agreement_set.count()

	def checkAndSendEmails(self):
		if self.agreers() >= self.threshold and (self.expiryDate is None or self.expiryDate >= timezone.now()) and self.stillOpen:
			self.sendEmails()

	def sendEmails(self):
		send_mail(
			'TCATCC Alert',
			'The item %s with description %s has met its threshold; act accordingly.' %(self.name,self.description),
			'diamond-grouping@example.com',
			list(Agreement.objects.filter(item=self)),
		)
		self.stillOpen = False
		self.save()

class Agreement(models.Model):
	email = models.EmailField()
	item = models.ForeignKey(Item, on_delete=models.CASCADE)

	def __str__(self):
		return "%s signup to %s" %(self.email, self.item.name)

	def save(self,*args,**kwargs):
		super().save(*args, **kwargs)
		self.item.checkAndSendEmails()
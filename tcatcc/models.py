from django.db import models
from django.utils import timezone

from django.contrib.auth.models import User

# Create your models here.
class Item(models.Model):
	name = models.TextField()
	description = models.TextField()
	owner = models.ForeignKey(User, on_delete=models.CASCADE)

	threshold = models.IntegerField()
	expiryDate =  models.DateTimeField(blank=True)

	stillOpen = models.BooleanField(default=True)

	def __str__(self):
		return self.name

	def agreers(self):
		return self.agreement_set.count()

	def checkAndSendEmails(self):
		if self.agreers() >= self.threshold and self.expiryDate >= timezone.now() and self.stillOpen:
			sendEmails()

	def sendEmails(self):
		print("Sending emails.")

class Agreement(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	item = models.ForeignKey(Item, on_delete=models.CASCADE)

	def __str__(self):
		return "%s signup to %s" %(self.user, self.item.name)

	def save(self,*args,**kwargs):
		self.item.checkAndSendEmails()
		super().save(*args, **kwargs)
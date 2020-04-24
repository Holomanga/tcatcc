from django.contrib import admin

# Register your models here.
from .models import Item, Agreement

admin.site.register(Agreement)

class AgreementsInLine(admin.TabularInline):
    model = Agreement

class ItemAdmin(admin.ModelAdmin):
	inlines = [AgreementsInLine]

admin.site.register(Item,ItemAdmin)
from django.urls import path
from . import views

app_name = 'tcatcc'
urlpatterns = [
	path('', views.index, name="index"),
	path('new', views.newItemView, name="create-item"),
	path('<int:itemid>', views.detailItemView, name="item-detail"),
	path('<uuid:uuid>', views.confirmSignupView, name="signup-confirmation")
]
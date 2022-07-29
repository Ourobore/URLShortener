from django.urls import path
from . import views

app_name = 'short_urls'
urlpatterns = [
    path('', views.index, name='index'),
    path('url_form', views.url_form, name='url_form'),
]
from django.urls import path
from . import views

app_name = 'short_urls'
urlpatterns = [
    path('', views.index, name='index'),
    path('<str:slug>', views.redirect_short_url, name='redirect_short_url')
]
"""MDGIVEMEMYREADINGLIST URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    path(
        '', 
        views.index, 
        name='index'
        ),
    path(
        'readlist', 
        views.readlist, 
        name='readlist'
    ),
    path(
        'return_reading_list_json', 
        views.return_reading_list_json, 
        name='return_reading_list_json'
    ),
    path(
        'download_reading_list_as_csv',
        views.download_reading_list_as_csv,
        name='download_reading_list_as_csv'
    ),
    path(
        'blank', 
        views.blank, 
        name='blank'
    ),
]

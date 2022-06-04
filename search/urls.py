from django.urls import path
from . import views

urlpatterns =[
    path('', views.SearchApiView.as_view(), name="search")
]
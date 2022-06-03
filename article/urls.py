from django.urls import path
from . import views


urlpatterns = [
    path('', views.articleListView, name='articles'),
    path('<str:pk>/', views.articleDetailView, name="get-article"),
]
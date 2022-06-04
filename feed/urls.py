from django.urls import path
from . import views

urlpatterns = [
     path('', views.feeds, name="feeds"),
     path('create/', views.createFeedView, name="createFeed"),
     path('edit/<str:pk>/', views.editFeedView, name="editFeed"),
     path('details/<str:pk>/', views.feedDetailView, name="feedDetails"),
     path('refeed/', views.refeedView, name="refeed"),
     path('vote/', views.voteUpdateView, name="vote"),
     path('delete/<str:pk>/', views.deleteFeedView, name="deleteFeed"),
     path('<str:pk>/comments/', views.feedCommentView, name="feedComment"),
]
from django.urls import path
from . import views


urlpatterns =[
    path('', views.articleListView, name='articles'),
    path('<str:pk>/', views.articleDetailView, name="get-article"),
    path('art/add/', views.create_article, name='create-article'),
    path('edit/<str:pk>/', views.articleUpdateView, name="edit-article"),
    path('delete/<str:pk>/', views.articleDeleteView, name="delete-article"),
    path('edit-comment/<str:pk>/', views.articleCommentUpdateView, name="edit-article-comment"),
    path('delete-comment/<str:pk>/', views.articleCommentDeleteView, name="delete-article-comment"),
    path('vote/', views.voteUpdateView, name='article-vote'),
    ]




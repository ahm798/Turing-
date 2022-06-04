from django.urls import path, include

urlpatterns = [
    path("api/articles/", include('article.urls')),
    path("api/search/", include("search.urls")),
    path("api/account/", include("account.urls")),
    path("api/feeds/", include("feed.urls")),

]
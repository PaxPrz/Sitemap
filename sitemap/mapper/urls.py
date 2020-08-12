from django.urls import path
from . import views

app_name = 'mapper'
urlpatterns = [
    path('', views.Sites.as_view(), name='sites'),
    path('<slug:slug>', views.sitemap_view, name='sitemap'),
]

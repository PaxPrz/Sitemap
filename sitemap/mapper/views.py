from django.shortcuts import render
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from .models import Site, Sitemap, Vulnerability

# Create your views here.
class Sites(ListView):
    model = Sites
    template = 'mapper/SitesListView.html'
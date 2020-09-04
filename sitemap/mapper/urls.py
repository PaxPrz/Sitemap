from django.urls import path
from . import views

app_name = 'mapper'
urlpatterns = [
    path('', views.Sites.as_view(), name='sites'),
    path('vuln/', views.getVulnForm, name="vulnform"),
    path('<slug:slug>/', views.sitemap_view, name='sitemap'),
    path('delete_site/', views.delete_site, name='deletesite'),
    path('<slug:slug>/addSite/', views.addSitemap, name="addSitemap"),
    path('<slug:slug>/deleteSitemap/', views.deleteSitemap, name="deleteSitemap"),
    path('getSitemap/<int:id>/', views.getSitemap, name="getSitemap"),
    path('<slug:slug>/editSitemap/<int:id>/', views.editSitemap, name="editSitemap"),
    path('<slug:slug>/<int:id>/getVulnerability/', views.getVulnerability, name="getVulnerability"),
    path('<slug:slug>/<int:id>/addVulnerability/', views.addVulnerability, name="addVulnerability"),
    path('<slug:slug>/getOneVuln/', views.getOneVuln, name="getonevuln"),
    path('<slug:slug>/editOneVuln/<int:vulnId>/', views.editOneVuln, name="editonevuln"),
    path('<slug:slug>/allvulns/',views.allVulnerability, name="allvulns"),
]

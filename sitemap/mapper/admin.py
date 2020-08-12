from django.contrib import admin
from .models import Site, Sitemap, Vulnerability

# Register your models here.
admin.site.register(Site)
admin.site.register(Sitemap)
admin.site.register(Vulnerability)
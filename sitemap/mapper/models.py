from django.db import models

# Create your models here.
class Site(db.Model):
    site_name = models.CharField(max_length=50)
    site_location = models.URLField(max_length=200)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.site_name

class Sitemap(db.Model):
    element = models.CharField(max_length=50)
    location = models.URLField(max_length=200)
    parent = models.ForeignKey(Sitemap, on_delete=models.CASCADE)
    require_login = models.BooleanField(default=False)
    site = models.ForeignKey(Site, on_delete=models.CASCADE)

    def __str__(self):
        return self.element

class Vulnerability(db.Model):
    sitemap = models.ForeignKey(Sitemap, on_delete=models.CASCADE)
    vulnerability = models.CharField(max_length=100)
    reported = models.BooleanField(default=False)
    fixed = models.BooleanField(default=False)

    def __str__(self):
        return self.vulnerability


from django.db import models
from django.utils.text import slugify

# Create your models here.
class Site(models.Model):
    site_name = models.CharField(max_length=50)
    site_location = models.URLField(max_length=200)
    is_active = models.BooleanField(default=True)
    slug = models.SlugField(max_length=50, unique=True)

    def __str__(self):
        return self.site_name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.site_name)
        super().save(*args, **kwargs)

class Sitemap(models.Model):
    element = models.CharField(max_length=50)
    location = models.URLField(max_length=200)
    parent = models.ForeignKey("Sitemap", on_delete=models.CASCADE, null=True)
    require_login = models.BooleanField(default=False)
    site = models.ForeignKey(Site, on_delete=models.CASCADE)
    comment = models.CharField(max_length=500, null=True, blank=True)

    def __str__(self):
        return self.element

VULN_CATEGORIES = (
    ('Critical', 'CRITICAL'),
    ('High', 'HIGH'),
    ('Medium', 'MEDIUM'),
    ('Low', 'LOW'),
    ('Informational', 'INFORMATIONAL'),
)

class Vulnerability(models.Model):
    sitemap = models.ForeignKey(Sitemap, on_delete=models.CASCADE)
    vulnerability = models.CharField(max_length=300)
    request = models.CharField(max_length=1000, null=True, blank=True)
    is_reported = models.BooleanField(default=False)
    is_fixed = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    category = models.CharField(max_length=15, choices=VULN_CATEGORIES, default='Low', null=True)

    def __str__(self):
        return self.vulnerability


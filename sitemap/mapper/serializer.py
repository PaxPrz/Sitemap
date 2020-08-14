from rest_framework import serializers
from .models import Sitemap

class SitemapSerializer(serializers.ModelSerializer):
    parent = serializers.RelatedField(read_only=True)

    class Meta:
        model = Sitemap
        fields = ('element', 'location', 'parent', 'require_login', 'comment')
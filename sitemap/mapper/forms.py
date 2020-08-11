from django import forms
from django.forms import formset_factory
from .models import Site, Sitemap, Vulnerability

class SiteForm(forms.ModelForm):
    site_name = forms.CharField(label="Site Name", widget=forms.TextInput(
        attrs={
            'class':'form-control',
            'placeholder':'Site Name'
        }
    ))
    site_location = forms.URLField(label="Site URL", required=False, widget=forms.TextInput(
        attrs={
            'class':'form-control',
            'placeholder':'Site URL'
        }
    ))
    is_active = forms.BooleanField(label="Site Active", required=False)

    class Meta:
        model = Site
        fields = ('site_name', 'site_location', 'is_active')

SiteFormset = formset_factory(SiteForm, extra=1)
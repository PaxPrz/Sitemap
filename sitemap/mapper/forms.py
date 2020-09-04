from django import forms
from django.forms import formset_factory
from .models import Site, Sitemap, Vulnerability, VULN_CATEGORIES

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

class VulnerabilityForm(forms.ModelForm):
    vulnerability = forms.CharField(label="Vulnerability", widget=forms.TextInput(
        attrs = {
            'class':'form-control',
            'placeholder':'Bug title'
        }
    ))
    category = forms.ChoiceField(label="Severity", choices=VULN_CATEGORIES, required=False, widget=forms.Select(
        attrs={
            'class':'form-control',
        }
    ))
    request = forms.CharField(label="Request/Comments", max_length=999, required=False, widget=forms.Textarea(
        attrs={
            'class':'form-control',
            'width':'50%',
            'height': '60px',
        }
    ))
    is_reported = forms.BooleanField(label="Is Reported?", required=False, widget=forms.CheckboxInput(
        attrs={
            'class':'form-control',
        }
    ))
    is_fixed = forms.BooleanField(label="Is Fixed?", required=False, widget=forms.CheckboxInput(
        attrs={
            'class':'form-control',
        }
    ))

    class Meta:
        model = Vulnerability
        fields = ('vulnerability', 'category', 'request', 'is_reported', 'is_fixed')

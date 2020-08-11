from django.shortcuts import render, redirect, reverse
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.core.exceptions import ObjectDoesNotExist

from .models import Site, Sitemap, Vulnerability
from .forms import SiteFormset, SiteForm

# Create your views here.
class Sites(ListView):
    model = Site
    template_name = 'mapper/SitesListView.html'
    context_object_name = 'sites'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = SiteForm(self.request.GET or None)
        return context

    # def post(self, **kwargs):
    #     formset = SiteFormset(self.request.POST)
    #     if formset.is_valid():
    #         for form in formset:
    #             site_name = form.cleaned_data.get('site_name')
    #             if site_name:
    #                 Site(site_name=site_name).save()

    def post(self, *args, **kwargs):
        form = SiteForm(self.request.POST)
        if form.is_valid():
            site_name = form.cleaned_data.get('site_name')
            try:
                q = Site.objects.get(site_name=site_name)
                nform = SiteForm(self.request.POST, instance=q)
                nform.save()
            except ObjectDoesNotExist:
                form.save()
        else:
            return render(self.request, 'mapper/SitesListView.html', {'form':form, 'sites':Site.objects.all()})
        return redirect('mapper:sites')
            


    
    
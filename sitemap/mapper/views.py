from django.shortcuts import render, redirect, reverse, get_object_or_404, HttpResponse
from django.http import JsonResponse
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers

from .models import Site, Sitemap, Vulnerability
from .forms import SiteFormset, SiteForm, VulnerabilityForm
from .serializer import SitemapSerializer


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
                m = form.save()
                rootEle = Sitemap.objects.create(element='/', location=m.site_location, site=m)
        else:
            return render(self.request, 'mapper/SitesListView.html', {'form':form, 'sites':Site.objects.all()})
        return redirect('mapper:sites')
            

def findSubEle(ele):
    eleList=[(ele, 0)]
    i=0
    while i < len(eleList):
        prev_indent = eleList[i][1]
        for ele in reversed(eleList[i][0].sitemap_set.all()):
            eleList.insert(i+1, (ele, prev_indent+1))
        i+=1
    return eleList

def sitemap_view(request, slug):
    site = get_object_or_404(Site, slug=slug)
    rootEle = get_object_or_404(Sitemap, element='/', site=site, parent=None)
    # print('Went inside')
    eleList=findSubEle(rootEle)
    # print('=============================')
    # print(eleList)
    # print('=============================')
    return render(request, 'mapper/SitemapView.html', {'eleList':eleList, 'site':site})

@csrf_exempt
def delete_site(request):
    if request.method == "POST":
        pid = request.POST.get('pk')
        site = get_object_or_404(Site, pk=pid)
        site.delete()
        return redirect('mapper:sites')

@csrf_exempt
def addSitemap(request, slug):
    if request.method == "POST":
        site = get_object_or_404(Site, slug=slug)
        element = request.POST.get('element')
        location = request.POST.get('location')
        parent = get_object_or_404(Sitemap, pk=int(request.POST.get('parent')))
        requireLogin = True if request.POST.get('requireLogin')!=None else False
        comment = request.POST.get('comment')

        Sitemap.objects.create(element=element, location=location, parent=parent, require_login=requireLogin, site=site, comment=comment)

        return redirect('mapper:sitemap', slug=slug)

@csrf_exempt
def deleteSitemap(request, slug):
    if request.method == "POST":
        id = int(request.POST.get('id'))
        sitemap = get_object_or_404(Sitemap, pk=id)
        sitemap.delete()
        return redirect('mapper:sitemap', slug=slug)

def getSitemap(request, id):
    if request.method == "GET":
        sitemap = get_object_or_404(Sitemap, pk=id)
        d = {'element':sitemap.element, 'location':sitemap.location, 'parent':sitemap.parent.element, 'require_login':sitemap.require_login, 'comment':sitemap.comment, 'parentpk':sitemap.parent.id}
        return JsonResponse(d)

@csrf_exempt
def editSitemap(request, slug, id):
    if request.method == "POST":
        print(id)
        print(request.POST)
        element = request.POST.get('element')
        location = request.POST.get('location')
        comment = request.POST.get('comment')
        reqLogin = request.POST.get('requireLogin')
        print(element, location, comment, reqLogin)
        s = get_object_or_404(Sitemap, pk=id)
        s.element = element
        s.location = location
        s.comment = comment
        s.require_login = bool(reqLogin)
        s.save()
        return redirect('mapper:sitemap', slug=slug)

def getVulnerability(request, slug, id):
    if request.method == "GET":
        sitemap = get_object_or_404(Sitemap, pk=id)
        vulnerability = sitemap.vulnerability_set.all()
        return JsonResponse(serializers.serialize('json', vulnerability), safe=False)

def getVulnForm(request):
    if request.method == "GET":
        vuln = VulnerabilityForm()
        return render(request, 'mapper/vulnform.html', {"form":vuln})
    elif request.method == "POST":
        print(request.POST)
        vuln = VulnerabilityForm(request.POST)
        if vuln.is_valid():
            print("VALID FORM")
        else:
            print("INVALID FORM")
        return render(request, 'mapper/vulnform.html', {"form":vuln})

@csrf_exempt
def addVulnerability(request, slug, id):
    if request.method == "GET":
        vuln = VulnerabilityForm()
        return JsonResponse({"form":vuln.as_p()})
    elif request.method == "POST":
        vuln = VulnerabilityForm(request.POST)
        if vuln.is_valid():
            print('vulnform valid')
            v = vuln.save(commit=False)
            v.sitemap = get_object_or_404(Sitemap, pk=id)
            v.save()
        else:
            print('forminvalid')
        return redirect('mapper:sitemap', slug=slug)

def getOneVuln(request, slug):
    if request.method == "GET":
        id = request.GET.get('id')
        vuln = get_object_or_404(Vulnerability, pk=id)
        if vuln:
            return JsonResponse({
                'id': vuln.id,
                'vulnerability': vuln.vulnerability,
                'request': vuln.request,
                'is_reported': vuln.is_reported,
                'is_fixed': vuln.is_fixed,
                'category': vuln.category
            })
        return JsonResponse({'message':'not found'})

@csrf_exempt
def editOneVuln(request, slug, vulnId):
    if request.method == "POST":
        vuln = get_object_or_404(Vulnerability, pk=int(vulnId))
        vuln.vulnerability = request.POST.get('vulnerability')
        vuln.request = request.POST.get('request')
        vuln.is_reported = True if request.POST.get('is_reported') else False
        vuln.is_fixed = True if request.POST.get('is_fixed') else False
        vuln.category = request.POST.get('category')
        vuln.save()
    return redirect('mapper:sitemap', slug=slug)

def allVulnerability(request, slug):
    if request.method == "GET":
        site = get_object_or_404(Site, slug=slug)
        allv = []
        for s in site.sitemap_set.all():
            allv += s.vulnerability_set.all()
        return render(request, 'mapper/allvulns.html', {'allv':allv})
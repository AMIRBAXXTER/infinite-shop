from django.contrib.postgres.search import TrigramSimilarity
from django.db.models import Count
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.generic import View
from IndexApp.forms import SearchForm
from IndexApp.models import *
from ProductsApp.models import Product, Category


# Create your views here.

class Index(View):
    template_name = 'index_app/index.html'

    def get(self, request):
        site_info = SiteInfo.objects.filter(is_active=True).first()
        main_pictures = MainPictures.objects.filter(site_info=site_info).all()
        side_pictures = SidePicture.objects.filter(site_info=site_info).all()
        featured_products = Product.objects.filter(is_active=True).order_by('-average_rate')[:4]
        off_products = Product.objects.filter(is_active=True).order_by('-off_percent')[:4]
        most_viewed_products = Product.objects.filter(is_active=True).annotate(
            num_visits=Count('product_visited')).order_by('-num_visits')[:4]
        context = {
            'main_pictures': main_pictures,
            'side_pictures': side_pictures,
            'featured_products': featured_products,
            'off_products': off_products,
            'most_viewed_products': most_viewed_products,

        }
        return render(request, self.template_name, context)


class AboutUs(View):
    template_name = 'index_app/about_us.html'

    def get(self, request):
        site_info = SiteInfo.objects.filter(is_active=True).first()
        team_members = TeamMember.objects.filter(site_info=site_info)
        context = {
            'site_info': site_info,
            'team_members': team_members
        }
        return render(request, self.template_name, context)


def header(request):
    site_info: SiteInfo = SiteInfo.objects.filter(is_active=True).first()
    context = {
        'site_info': site_info
    }
    return render(request, 'infinite shop/partial/header.html', context)


def footer(request):
    site_info: SiteInfo = SiteInfo.objects.filter(is_active=True).first()
    main_categories = Category.objects.filter().all().order_by('?')[:8]
    context = {
        'site_info': site_info,
        'main_categories': main_categories
    }
    return render(request, 'infinite shop/partial/footer.html', context)


class Search(View):
    template_name = 'index_app/search.html'

    def post(self, request):
        query = request.POST.get('query')
        if query:
            # result1 = Product.objects.annotate(similarity=TrigramSimilarity('title', query)).filter(similarity__gt=0.1)
            # result2 = Product.objects.annotate(similarity=TrigramSimilarity('short_description', query)).filter(
            #     similarity__gt=0.01)
            # products = (result1 | result2).order_by('-similarity')

            # search structure changed, because server cant install trigram extension.
            result1 = Product.objects.filter(title__icontains=query).order_by('sale_count')
            result2 = Product.objects.filter(short_description__icontains=query).order_by('sale_count')
            result3 = Product.objects.filter(long_description__icontains=query).order_by('sale_count')
            result4 = Product.objects.filter(brand__title__icontains=query).order_by('sale_count')
            result5 = Product.objects.filter(category__title__icontains=query).order_by('sale_count')
            result6 = Product.objects.filter(category__parent__title__icontains=query).order_by('sale_count')
            products = (result1 | result2 | result3 | result4 | result5 | result6).distinct().order_by('sale_count')
            context = {
                'products': products,
                'query': query
            }
            return render(request, self.template_name, context)
        return redirect('IndexApp:index')

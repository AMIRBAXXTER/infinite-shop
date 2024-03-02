from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.http import HttpRequest, Http404
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView
from django.http import JsonResponse
from IndexApp.models import SiteInfo
from .models import *


# Create your views here.
def product_detail(request: HttpRequest, product_id):
    product: Product = Product.objects.select_related('brand').prefetch_related('category',
                                                                                'rate',
                                                                                'comment').filter(
        id=product_id).first()
    user = request.user
    if product is None:
        raise Http404
    avg = int(product.average_rate)
    user_favorited = product.favorites.filter(user=user).exists()
    blank_star = 5 - avg
    main_category = product.category.filter(parent=None).first()
    product_comments = ProductComment.objects.filter(product=product, parent=None).order_by('-created_at')
    product_all_comments = ProductComment.objects.filter(product=product)
    product_color = ProductColor.objects.filter(product=product).first()
    product_properties = ProductProperty.objects.filter(product=product)
    related_products = Product.objects.filter(category__in=product.category.all()).order_by('-created_at').exclude(
        id=product.id).distinct()
    print(request.META.get('REMOTE_ADDR'))
    print(request.META.get('HTTP_X_FORWARDED_FOR'))

    if request.method == 'GET':
        ip = request.META.get('REMOTE_ADDR') or request.META.get('HTTP_X_FORWARDED_FOR')
        if ip not in product.product_visited.all().values_list('ip', flat=True):
            ProductVisited(product=product, ip=ip, user=request.user if request.user.is_authenticated else None).save()

    context = {
        'product': product,
        'star_range': range(1, (avg + 1)),
        'blank_star': range(1, (blank_star + 1)),
        'main_category': main_category,
        'product_comments': product_comments,
        'product_all_comments': product_all_comments,
        'product_color': product_color,
        'product_properties': product_properties,
        'related_products': related_products,
        'user_favorited': user_favorited,

    }
    return render(request, 'products_app/product_detail.html', context)


class ProductListView(ListView):
    model = Product
    template_name = 'products_app/product_list.html'
    context_object_name = 'products'
    ordering = 'title'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        site_info = SiteInfo.objects.filter(is_active=True).first()
        main_category = Category.objects.filter(parent=None).all()
        brands = Brand.objects.all()
        most_expensive = Product.objects.order_by('-final_price').first()
        context['site_info'] = site_info
        context['main_category'] = main_category
        context['brands'] = brands
        context['most_expensive'] = most_expensive
        return context

    def get_queryset(self):
        query = super(ProductListView, self).get_queryset()
        order_by = self.request.GET.get('order-by')
        low_price = self.request.GET.get('low-price')
        high_price = self.request.GET.get('high-price')
        category = self.kwargs.get('category')
        brand = self.kwargs.get('brand')
        if brand:
            query = query.filter(brand__title__iexact=brand)

        if category:
            query = query.filter(category__url_title__iexact=category)
        if order_by:
            if order_by == 'available':
                query = query.filter(is_active=True)
            if order_by == 'newer':
                query = query.order_by('-created_at')
            elif order_by == 'high-price':
                query = query.order_by('-final_price')
            elif order_by == 'low-price':
                query = query.order_by('final_price')
            elif order_by == 'most-view':
                query = query.annotate(num_visits=Count('product_visited'))
                query = query.order_by('-num_visits')
            elif order_by == 'most-sale':
                query = query.order_by('-sale_count')

        if low_price or high_price:
            query = query.filter(final_price__gte=low_price, final_price__lte=high_price)

        return query


def color_stock(request: HttpRequest):
    product_id = request.GET.get('product_id')
    product_color = request.GET.get('product_color')
    product = Product.objects.filter(id=product_id).first()
    stock = ProductColor.objects.filter(product=product, color=product_color).first()
    response = {
        'stock': stock.stock,
        'title': stock.title,
        'color': stock.color,
    }
    return JsonResponse(response)


@login_required
def product_comment(request: HttpRequest):
    product_id = request.GET.get('product_id')
    product = Product.objects.filter(id=product_id).first()
    comment = request.GET.get('comment')
    user = request.user
    parent_id = request.GET.get('parent')
    parent = ProductComment.objects.filter(id=parent_id).first() if parent_id else None
    new_comment = ProductComment(product=product, user=user, comment=comment, parent=parent)
    new_comment.save()
    comments = ProductComment.objects.filter(product=product, parent=None).order_by('-created_at')

    context = {
        'product_comments': comments
    }
    return render(request, 'partials/comments_partial.html', context)

@login_required
def add_product_to_favorite(request):
    product_id = request.GET.get('product_id')
    product: Product = Product.objects.filter(id=product_id).first()
    user = request.user
    if not product.favorites.filter(user=user).exists():
        product.favorites.create(user=user)
        return JsonResponse({'liked': True})

    else:
        product.favorites.filter(user=user).delete()
        return JsonResponse({'liked': False})


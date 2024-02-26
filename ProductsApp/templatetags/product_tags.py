from django import template
register = template.Library()

@register.filter
def product_main_image(product):
    return product.product_images.filter(is_main=True).first().image.url

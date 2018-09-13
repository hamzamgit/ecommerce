from django.template import Library
from products.models import ProductModel

register = Library()


@register.filter()
def calculate_discount(p):
    discount = (p.product_discount) * 100 / p.product_price
    return '{}%'.format((discount).__round__(1))


# @register.filter()
# def calculate_discount2(p):
#     return '{}%'.format((p[1] * 100 / p[0]).__round__(1))
#     # return '{}%'.format((d * 100 / p).__round__(1))


@register.filter()
def availability_status(o):
    return "Available in Stock" if o > 0 else "Not Available Right Now"


@register.filter()
def discounted_price(o):
    return o.product_price - o.product_discount


@register.filter()
def is_even(a):
    return a % 2 == 0


@register.filter()
def get_filtered_products(name: str):
    # return ProductModel.product_company.objects.filter(company_name=name)
    return ProductModel.objects.filter(product_company__company_name=name)


@register.filter()
def get_array(val):
    return list(range(0, val))

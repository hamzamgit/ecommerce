from django.urls import path
from django.conf.urls import url
from .views import *
from django.conf import settings
from django.conf.urls.static import static

app_name = 'products'

urlpatterns = [
    path('', IndexView.as_view(), name='Index'),
    path('products/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('get-products/', get_products, name='get-products'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

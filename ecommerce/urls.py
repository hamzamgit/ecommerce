from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from products.views import view_404

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('products.urls', namespace='products')),
    url(r'^', view_404, name='Error404')
]

# handler404 = 'products.views.view_404'

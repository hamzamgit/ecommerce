from django.http import HttpResponseRedirect, JsonResponse, Http404
from django.shortcuts import reverse, get_object_or_404, render
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView, FormView
from products.models import *
from products.forms import RatingModelForm
from django.core.serializers import serialize


class IndexView(TemplateView):
    template_name = 'products/index.html'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['banner'] = BannerModel.objects.filter(banner_active=True)
        context['products'] = ProductModel.objects.all()
        context['companies'] = CompanyModel.objects.all()
        return context


@csrf_exempt
def get_products(request):
    send = None
    if request.method != 'POST':
        return JsonResponse(None, safe=False)
    if request.method == 'POST':
        if request.POST['name']:
            send = ProductModel.objects.filter(product_company__company_name=request.POST['name'])[:6]
            # send = ProductModel.product_company.objects.filter(company_name=request.POST['name'])
            data = serialize('json', send)

        return JsonResponse(data, safe=False)


class ProductDetailView(FormView):
    template_name = 'products/product_detail.html'
    form_class = RatingModelForm

    def dispatch(self, request, *args, **kwargs):
        try:
            self.object = ProductModel.objects.get(pk=self.kwargs['pk'])
        except ProductModel.DoesNotExist:
            return view_404(request, context={"status": "Error", "reason": "Product for the provided"
                                                                           " ID doeasn't exist"})
        except:
            return view_404(request, context={"status": "Error", "reason": "An error occured while "
                                                                           "retrieving the product"})
        return super(ProductDetailView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ProductDetailView, self).get_context_data(**kwargs)
        context['product'] = self.object
        context['products'] = ProductModel.objects.all()
        return context

    def form_valid(self, form):
        review = form.save(commit=True)
        try:
            this_product = get_object_or_404(ProductModel, pk=self.kwargs['pk'])
        except Http404:
            return view_404(self.request, {"status": "Error", "reason":"Product against the provided ID doesn't exist!"})
        this_product.product_review.add(review)
        this_product.save()
        return HttpResponseRedirect(reverse('products:product_detail', args=[self.kwargs['pk']]))


def view_404(request, context=None):
    if context is None:
        context = {"status": "Error", "reason":"We were unable to fetch the page requested!"}
    return render(request, '404.html', context)

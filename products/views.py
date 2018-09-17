from django.core.serializers import serialize
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import reverse, get_object_or_404, render
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView, FormView
from django.contrib import messages
from products.models import *
from products.forms import RatingModelForm


class IndexView(TemplateView):
    template_name = 'products/index.html'
    http_method_names = ['get']

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['banner'] = BannerModel.objects.filter(banner_active=True)
        context['products'] = ProductModel.objects.all()
        context['companies'] = CompanyModel.objects.all()
        return context


@csrf_exempt
def get_products(request):
    send = ''
    if request.method != 'POST':
        return JsonResponse(None, safe=False)
    if request.method == 'POST' and request.POST['name']:
        if request.POST['name'] == 'All':
            send = ProductModel.objects.all()
        else:
            send = ProductModel.objects.filter(product_company__company_name=request.POST['name'])[:6]
        data = serialize('json', send)
        return JsonResponse(data, safe=False)


class ProductDetailView(FormView):
    template_name = 'products/product_detail.html'
    form_class = RatingModelForm

    def dispatch(self, request, *args, **kwargs):
        try:
            self.object = ProductModel.objects.get(pk=self.kwargs['pk'])
        except ProductModel.DoesNotExist:
            return view_404(request, context={"status": "Error 404", "reason": "Product for the provided"
                                                                               " ID doeasn't exist"})
        # except ProductModel.MultipleObjectsReturned:
        #     return view_404(request, context={"status": "Error 404", "reason": "An error occured while "
        #                                                                        "retrieving the product"})
        return super(ProductDetailView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        print(self.request)
        context = super(ProductDetailView, self).get_context_data(**kwargs)
        context['product'] = self.object
        context['products'] = ProductModel.objects.all()
        return context

    def form_invalid(self, form):
        errors = {
            'rating_user': 'Choose a Usename',
            'rating_title': 'Enter Title',
            'rating_review': 'Enter Review',
            'rating_rating': 'Tick any Rating Star',
        }
        for er in form.errors:
            form.errors[er][0] = errors[er]
        return super().form_invalid(form)

    def form_valid(self, form):
        review = form.save(commit=True)
        this_product = get_object_or_404(ProductModel, pk=self.kwargs['pk'])
        this_product.product_review.add(review)
        this_product.save()
        messages.success(self.request, "Review Submitted Successfully")
        return HttpResponseRedirect(
            reverse('products:product_detail', args=[self.kwargs['pk']]) + '?active_tab=reviews')


def view_404(request, context=None):
    if context is None:
        context = {"status": "Error 404", "reason": "We were unable to fetch the page requested!"}
    return render(request, '404.html', context)

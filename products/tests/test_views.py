from django.urls import reverse
from django.test import Client, TestCase
from django.test.utils import setup_test_environment, teardown_test_environment
from products.models import *
from products.forms import RatingModelForm
from model_mommy import mommy


# teardown_test_environment()
# setup_test_environment()


def create_products():
    return mommy.make(ProductModel)


def create_company():
    return mommy.make(CompanyModel)


def create_banner():
    return mommy.make(BannerModel)


class TestIndex(TestCase):

    def test_index_view_get(self):
        create_products()
        create_banner()
        create_company()
        response = self.client.get(reverse('products:Index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'products/index.html')
        self.assertEqual(len(response.context['products']), len(ProductModel.objects.all()))
        self.assertEqual(len(response.context['banner']), len(BannerModel.objects.filter(banner_active=True)))
        self.assertEqual(len(response.context['companies']), len(CompanyModel.objects.all()))

    def test_index_view_post(self):
        response = self.client.post(reverse('products:Index'))
        self.assertEqual(response.status_code, 405)


class TestDetailView(TestCase):

    def test_product_detail_get(self):
        obj = create_products()
        response = self.client.get(reverse('products:product_detail', args=[obj.id]))
        self.assertTemplateUsed(response, 'products/product_detail.html')
        self.assertEqual(response.status_code, 200)

    def test_product_detail_post_valid(self):
        user = mommy.make(User)
        rating = mommy.make(RatingAndReviewModel, rating_user=user)
        # rating = RatingAndReviewModel.object.get(id=1)
        data = {
            'rating_user': rating.rating_user_id,
            'rating_title': 'rating.rating_title',
            'rating_review': rating.rating_review,
            'rating_rating': 4
        }
        product = create_products()
        response = self.client.post(reverse('products:product_detail', args=[product.id]), data=data)
        self.assertRedirects(response, reverse('products:product_detail', args=[product.id]) + '?active_tab=reviews')

    def test_product_detail_post_invalid(self):
        user = mommy.make(User)
        rating = mommy.make(RatingAndReviewModel, rating_user=user)
        # rating = RatingAndReviewModel.object.get(id=1)
        data = {
            'rating_user': None,
            'rating_title': None,
            'rating_review': None,
            'rating_rating': None
        }
        errors = {
            'rating_user': 'Choose a Usename',
            'rating_title': 'Enter Title',
            'rating_review': 'Enter Review',
            'rating_rating': 'Tick any Rating Star',
        }
        product = create_products()
        response = self.client.post(reverse('products:product_detail', args=[product.id]), data=data)
        self.assertTemplateUsed(response, 'products/product_detail.html')
        for er in response.context['form'].errors:
            self.assertEquals(response.context['form'].errors[er][0], errors[er])

    def test_product_detail_post_404(self):
        user = mommy.make(User)
        rating = mommy.make(RatingAndReviewModel, rating_user=user)
        # rating = RatingAndReviewModel.object.get(id=1)
        data = {
            'rating_user': rating.rating_user_id,
            'rating_title': 'rating.rating_title',
            'rating_review': rating.rating_review,
            'rating_rating': 7
        }
        product = create_products()
        response = self.client.post(reverse('products:product_detail', args=[product.id]), data=data)
        self.assertTemplateUsed(response, 'products/product_detail.html')

    def test_product_except_404(self):
        response = self.client.get(reverse('products:product_detail', args=[92384]))
        self.assertTemplateUsed(response, '404.html')
        self.assertEquals(response.context['status'], "Error 404")
        self.assertEquals(response.context['reason'], "Product for the provided ID doeasn't exist")

    def product_except_multiple(self):
        prod = mommy.make(ProductModel, product_name=9)
        prods = mommy.make(ProductModel, product_name=9)
        response = self.client.get(reverse('products:product_detail', args=[prod.product_name]))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, '404.html')
        self.assertEquals(response.context['status'], "Error 404")
        self.assertEquals(response.context['reason'], "An error occured while retrieving the product")


class Test404(TestCase):

    def test_view_404_get(self):
        response = self.client.get('/233')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, '404.html')
        self.assertEquals(response.context['status'], "Error 404")
        self.assertEquals(response.context['reason'], "We were unable to fetch the page requested!")

    def test_view_404_post(self):
        self.assertEqual(self.client.post(reverse('Error404')).status_code, 405)


class TestGetProducts(TestCase):

    def test_get_products_get(self):
        response = self.client.get(reverse('products:get-products'))
        self.assertEqual(response.status_code, 200)

    def test_get_products_post(self):
        company = create_company()
        product = mommy.make(ProductModel, product_company=company)
        response = self.client.post(reverse('products:get-products'), data={'name': company.company_name})
        self.assertEqual(response.status_code, 200)

    def test_get_products_post_none(self):
        company = create_company()
        product = mommy.make(ProductModel, product_company=company)
        response = self.client.post(reverse('products:get-products'), data={'name': None})
        self.assertEqual(response.content, b'"[]"')

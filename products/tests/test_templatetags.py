from django.test import TestCase
from products.templatetags import extras
from products.models import *
from model_mommy import mommy


class TestTemplateTags(TestCase):

    # def calculate_discount(p):
    #     discount = (p.product_discount) * 100 / p.product_price
    #     return '{}%'.format((discount).__round__(1))

    def test_calculate_discount(self):
        p = mommy.make(ProductModel, product_discount=50, product_price=600)
        self.assertEquals(extras.calculate_discount(p), '{}%'.format((p.product_discount * 100 / p.product_price)
                                                                     .__round__(1)))
        self.assertNotEquals(extras.calculate_discount(p), '{}'.format((p.product_discount * 100 / p.product_price)
                                                                       .__round__(1)))
        self.assertNotEquals(extras.calculate_discount(p), '{}%'.format((p.product_discount * 100 / p.product_price)))

    def test_availability_status(self):
        self.assertEquals(extras.availability_status(5), 'Available in Stock')
        self.assertEquals(extras.availability_status(-2), 'Not Available Right Now')
        self.assertEquals(extras.availability_status(0), 'Not Available Right Now')

    def test_discounted_price(self):
        p = mommy.make(ProductModel, product_discount=50, product_price=600)
        self.assertEquals(extras.discounted_price(p), p.product_price - p.product_discount)

    def test_is_even(self):
        self.assertTrue(extras.is_even(6))
        self.assertFalse(extras.is_even(9))
        self.assertTrue(extras.is_even(0))

    def test_get_filtered_products(self):
        company = mommy.make(CompanyModel, company_name='Test')
        mommy.make(ProductModel, product_company=company, _quantity=3)
        self.assertEquals(len(extras.get_filtered_products(company.company_name)),
                          len(ProductModel.objects.filter(product_company__company_name="Test")))

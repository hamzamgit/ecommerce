from django.test import TestCase
from django.db.utils import IntegrityError,DataError
from products.models import *
from model_mommy import mommy


class TestModels(TestCase):

    # BannerModel Tests

    def test_banner_create(self):
        with self.assertRaises(DataError):
            mommy.make(BannerModel,
                banner_title='asldfjasldfjljweqporuqwenzlsvapsodiqpwierpqweoiraskldjfalsdnfoqiweuro')

    def test_banner_str(self):
        banner = mommy.make(BannerModel, banner_title='Test')
        self.assertEqual(banner.__str__(), 'Test')
    #
    # def test_banner_background_image(self):
    #     file = SimpleUploadedFile(name='test.txt', content=b'This is a file', content_type='text/plain')
    #     with self.assertRaises(ValidationError):
    #         mommy.make(BannerModel, banner_image=file)

    # ProductDetailModel Tests

    def test_product_detail_str(self):
        product_detail = mommy.make(ProductDetailsModel, detail_title='testing')
        self.assertEqual(product_detail.__str__(), 'testing')

    # ProductModel Tests

    def test_product_str(self):
        product = mommy.make(ProductModel, product_name='title')
        self.assertEqual(product.__str__(), 'title')

    # CompanyModel Tests
    def test_company_str(self):
        company = mommy.make(CompanyModel, company_name='company_title')
        self.assertEqual(company.__str__(), 'company_title')

    # CategoriesModel Tests
    def test_categories_str(self):
        cate = mommy.make(CategoriesModel, category_name='electronic')
        self.assertEqual(cate.__str__(), 'electronic')

    # RatingandReviewModel Tests
    # def test_rating_and_review_max_min(self):
    #     with self.assertRaises(Error):
    #         mommy.make(RatingAndReviewModel, rating_rating=7)

    def test_rating_and_review_str(self):
        rating = mommy.make(RatingAndReviewModel, rating_title='rating_title')
        self.assertEqual(rating.__str__(), 'rating_title')


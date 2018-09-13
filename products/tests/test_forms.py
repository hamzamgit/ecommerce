from django.test import TestCase
from products.forms import RatingModelForm
from products.models import *
from model_mommy import mommy


class TestRatingForm(TestCase):

    def test_form_valid(self):
        user = mommy.make(User)
        rating = mommy.make(RatingAndReviewModel, rating_user=user)
        # rating = RatingAndReviewModel.object.get(id=1)
        data = {
            'rating_user': rating.rating_user_id,
            'rating_title': 'rating.rating_title',
            'rating_review': rating.rating_review,
            'rating_rating': 4
        }
        ratingform = RatingModelForm(data=data)
        self.assertTrue(ratingform.is_valid())

    def test_form_invalid_max_choice(self):
        user = mommy.make(User)
        rating = mommy.make(RatingAndReviewModel, rating_user=user)
        # rating = RatingAndReviewModel.object.get(id=1)
        data = {
            'rating_user': rating.rating_user_id,
            'rating_title': 'rating.rating_title',
            'rating_review': rating.rating_review,
            'rating_rating': 7
        }
        ratingform = RatingModelForm(data=data)
        self.assertFalse(ratingform.is_valid())
        self.assertEquals(ratingform.errors['rating_rating'],
                          ['Select a valid choice. {} is not one of the available choices.'.format(
                              data['rating_rating'])])

    def test_form_invalid_min_choice(self):
        user = mommy.make(User)
        rating = mommy.make(RatingAndReviewModel, rating_user=user)
        # rating = RatingAndReviewModel.object.get(id=1)
        data = {
            'rating_user': rating.rating_user_id,
            'rating_title': 'rating.rating_title',
            'rating_review': rating.rating_review,
            'rating_rating': 0
        }
        ratingform = RatingModelForm(data=data)
        self.assertFalse(ratingform.is_valid())
        self.assertEquals(ratingform.errors['rating_rating'],
                          ['Select a valid choice. {} is not one of the available choices.'.format(
                              data['rating_rating'])])


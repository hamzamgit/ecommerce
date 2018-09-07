import uuid
from django.db import models
from django.utils import timezone
from django.core.validators import (MaxValueValidator, MinValueValidator, FileExtensionValidator)
from django.contrib.auth.models import User


class BannerModel(models.Model):
    banner_title = models.CharField(max_length=50)
    banner_description = models.TextField()
    banner_background_image = models.FileField(upload_to='banner/bgimage')
    banner_image = models.FileField(upload_to='banner/image', validators=[
        FileExtensionValidator(allowed_extensions=['jpg', 'png', 'gif'])])
    banner_active = models.BooleanField(default=True)

    objects = models.Manager

    def __str__(self):
        # return self.banner_title
        return '{}'.format(self.banner_title)


class ProductDetailsModel(models.Model):
    detail_title = models.CharField(max_length=50)
    detail_description = models.TextField()
    detail_image = models.ImageField(blank=True, null=True, upload_to='details/images')

    def __str__(self):
        return self.detail_title


class RatingAndReviewModel(models.Model):
    rating_user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating_title = models.CharField(max_length=50)
    rating_review = models.TextField()
    rating_time = models.DateTimeField(default=timezone.now)
    rating_rating = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)])

    def __str__(self):
        return self.rating_title


class CategoriesModel(models.Model):
    category_name = models.CharField(max_length=50)
    category_parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.category_name


class CompanyModel(models.Model):
    company_name = models.CharField(max_length=30)
    company_active = models.BooleanField(default=True)

    def __str__(self):
        return self.company_name


class ProductModel(models.Model):
    product_name = models.CharField(max_length=50)
    product_Description = models.TextField()
    product_available = models.PositiveIntegerField(default=1)
    product_price = models.FloatField()
    product_discount = models.FloatField()
    product_image = models.ImageField(upload_to='products/')
    product_detail = models.ManyToManyField(ProductDetailsModel, blank=True)
    product_review = models.ManyToManyField(RatingAndReviewModel, blank=True)
    product_company = models.ForeignKey(CompanyModel, on_delete=models.PROTECT)
    product_category = models.ForeignKey(CategoriesModel, on_delete=models.PROTECT)

    def __str__(self):
        return self.product_name


class People(models.Model):
    name = models.CharField(max_length=40)
    gender = models.CharField(max_length=1)
    User_id = models.UUIDField(default=uuid.uuid4())

    class Meta:
        abstract = True


class MaleManager(models.Manager):
    def get_queryset(self):
        return super(MaleManager, self).get_queryset().filter(gender='M')

#
# class Male(People):
#     objects = MaleManager()
#
#     class Meta:
#         proxy = True


class NewModel(People):
    new_field = models.GenericIPAddressField()


class A(models.Model):
    afield = models.CharField(max_length=5)
    bfield = models.CharField(max_length=5)

    def __str__(self):
        return "{} {}".format(self.afield, self.bfield)


class B (A):
    cfield = models.CharField(max_length=5)

    def __str__(self):
        return "{} {}".format(self.afield, self.bfield, self.cfield)


# Generated by Django 2.1 on 2018-09-03 13:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0009_categoriesmodel'),
    ]

    operations = [
        migrations.AlterField(
            model_name='categoriesmodel',
            name='category_subcategory',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='products.CategoriesModel'),
        ),
    ]

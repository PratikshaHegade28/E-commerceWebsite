# Generated by Django 5.1.1 on 2024-12-14 08:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0012_remove_product_nutritional_info_product_discription'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='discount',
            field=models.IntegerField(default=0),
        ),
    ]

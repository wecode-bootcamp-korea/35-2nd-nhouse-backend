# Generated by Django 4.0.6 on 2022-08-03 17:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('carts', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cart',
            old_name='option',
            new_name='product_option',
        ),
    ]

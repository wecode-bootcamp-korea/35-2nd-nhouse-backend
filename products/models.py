from django.db   import models

from core.models import TimeStampModel

class FirstCategory(models.Model):
    name = models.CharField(max_length=45)

    class Meta:
        db_table = 'first_categories'

class SecondCategory(models.Model):
    name           = models.CharField(max_length=45)
    first_category = models.ForeignKey(FirstCategory, on_delete=models.CASCADE)

    class Meta:
        db_table = 'second_categories'

class Color(models.Model):
    name = models.CharField(max_length=45)

    class Meta:
        db_table = 'colors'

class Size(models.Model):
    name = models.CharField(max_length=45)

    class Meta:
        db_table = 'sizes'

class Brand(models.Model):
    name = models.CharField(max_length=45)

    class Meta:
        db_table = 'brands'

class Product(TimeStampModel):
    title              = models.CharField(max_length=45)
    main_image         = models.URLField(max_length=300)
    price              = models.DecimalField(decimal_places=3, max_digits=10)
    brand              = models.ForeignKey(Brand, on_delete=models.CASCADE)
    second_category    = models.ForeignKey(SecondCategory, on_delete=models.CASCADE)
    additional_product = models.ManyToManyField('self', through='AdditionalProduct')

    class Meta:
        db_table = 'products'

class ProductOption(models.Model):
    additional_price = models.DecimalField(decimal_places=3, max_digits=10)
    stock            = models.IntegerField()
    product          = models.ForeignKey(Product, on_delete=models.CASCADE)
    size             = models.ForeignKey(Size, on_delete=models.CASCADE)
    color            = models.ForeignKey(Color, on_delete=models.CASCADE)

    class Meta:
        db_table = 'product_options'

class AdditionalProduct(models.Model):
    product            = models.ForeignKey(Product, on_delete=models.CASCADE,related_name='original_products')
    additional_product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='linked_products')

    class Meta:
        db_table = 'additional_products'

class DetailImage(models.Model):
    url     = models.URLField(max_length=300)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    class Meta:
        db_table = 'detail_images'

class ThumbnailImage(models.Model):
    url     = models.URLField(max_length=300)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    class Meta:
        db_table = 'thumbnail_images'

from django.http       import JsonResponse
from django.views      import View

from products.models import FirstCategory, Product, AdditionalProduct

class FirstCategoryView(View):
    def get(self, request):
        first_categories = FirstCategory.objects.all()

        results = [{
            'first_category_id'   : first_category.id,
            'first_category_title': first_category.name,
            'second_categories':[{
                'second_category_id'   : second_category.id,
                'second_category_title': second_category.name
            }for second_category in first_category.secondcategory_set.all()]
        }for first_category in first_categories]

        return JsonResponse({'results': results}, status=200)


class ProductDetailView(View):
    def get(self, request, product_id):
        products = Product.objects.filter(id=product_id)\
            .select_related("second_category__first_category","brand")\
            .prefetch_related('productoption_set__size','productoption_set__color','additional_product','thumbnailimage_set', 'additional_product__brand')

        result=[{
            'product_id' : product.id,
            'first_category' : [{
                    'first_category_id'  : product.second_category.first_category.id,
                    'first_category_name': product.second_category.first_category.name
                }],
            'second_category' : [{
                    'second_category_id'  : product.second_category.id,
                    'second_category_name': product.second_category.name
                }],
            'brand'          : product.brand.name,
            'title'          : product.title,
            'price'          : product.price,
            'thumbnail_images'    : [thumbnailimage.url for thumbnailimage in product.thumbnailimage_set.all()],
            'additional_products' : [{
                'id'    : additional_product.id,
                'brand' : {
                    'id'   : additional_product.brand.id,
                    'name' : additional_product.brand.name
                },
            } for additional_product in product.additional_product.all()],
            'product_options'    : [{
                'size_option'     : productoption.size.name,
                'color_option'    : productoption.color.name,
                'additional_price': productoption.additional_price
            }for productoption in product.productoption_set.all()]
        }for product in products]

        return JsonResponse({'result': result }, status=200)

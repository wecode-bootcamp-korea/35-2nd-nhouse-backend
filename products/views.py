from django.http            import JsonResponse
from django.views           import View
from django.db.models       import Q
from django.core.paginator  import Paginator
from django.core.exceptions import FieldError

from products.models       import FirstCategory, Product

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
        product = Product.objects\
            .select_related("second_category__first_category","brand")\
            .prefetch_related('productoption_set__size','productoption_set__color','additional_product','thumbnailimage_set')\
            .get(id = product_id)

        result={
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
            'additional_products' : [additional_product.title for additional_product in product.additional_product.all()],
            'product_options'    : [{
                'size_option'     : productoption.size.name,
                'color_option'    : productoption.color.name,
                'additional_price': productoption.additional_price
            }for productoption in product.productoption_set.all()]
        }

        return JsonResponse({'result': result }, status=200)


class ProductListView(View):
    def get(self, request):
        first_category_id  = request.GET.get('first_category')
        second_category_id = request.GET.get('second_category')
        color              = request.GET.get('color')
        size               = request.GET.get('size')
        sort               = request.GET.get('sort', 'id')
        limit              = int(request.GET.get("limit", 8))
        offset             = int(request.GET.get("offset", 1))

        product_Q = Q()

        if second_category_id:
            product_Q = Q(second_category = second_category_id)

        elif first_category_id:
            product_Q = Q(second_category__first_category_id = first_category_id)
        
        if color:
            product_Q &= Q(productoption__color__name=color)

        if size:
            product_Q &= Q(productoption__size__name=size)
        
        sort_menu={
            'id'        : 'id',
            'high_price': '-price',
            'low_price' : 'price',
            'best'      : 'productoption__stock'
            }

        if not sort in sort_menu:
            return JsonResponse({"message": "SORT_INVALID_VALUE"})
        
        products = Product.objects.filter(product_Q).order_by(sort_menu.get(sort))\
            .select_related('second_category__first_category','brand')

        p = Paginator(products, limit)

        results = [{
            'product_id'        : product.id,
            'title'             : product.title,
            'brand'             : product.brand.name,
            'price'             : product.price,
            'first_category_id' : product.second_category.first_category.id,
            'second_category_id': product.second_category.id,
            'main_image'        : product.main_image,
            }for product in p.page(offset)]

        return JsonResponse({"results":results, "exist_nest_page":p.page(offset).has_next()},status = 200)

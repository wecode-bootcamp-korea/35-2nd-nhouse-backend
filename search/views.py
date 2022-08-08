from django.http           import JsonResponse
from django.views          import View
from django.db.models      import Q
from django.core.paginator import Paginator

from products.models import Product, FirstCategory, SecondCategory

class ProductSearchView(View):
    def get(self, request):
        keyword = request.GET.get('keyword')
        limit   = int(request.GET.get('limit', 5))
        offset  = int(request.GET.get('offset', 1))

        queries = Q()

        if keyword:
            queries &= Q(title__icontains=keyword)

        products = Product.objects.filter(queries).select_related('brand').order_by('-created_at')
        
        p = Paginator(products, limit)
        pages_count = p.num_pages

        if offset < 1 or offset > pages_count:
            return JsonResponse({'result': 'INVALID_PAGE'}, status=404)

        total = {
            'total_items' : products.count(),
            'total_pages' : pages_count,
            'current_page': offset,
            'limit'       : limit
        }
        
        page_items = p.page(offset) 
        
        result = [{
            'id'        : page_item.id,
            'title'     : page_item.title,
            'main_image': page_item.main_image,
            'price'     : page_item.price,
            'brand'     : page_item.brand.name
        } for page_item in page_items]

        return JsonResponse({'total' : total, 'result' : result}, status=200)

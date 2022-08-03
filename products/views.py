from django.http       import JsonResponse
from django.views      import View

from products.models import FirstCategory

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
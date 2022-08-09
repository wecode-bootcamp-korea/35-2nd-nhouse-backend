from django.http           import JsonResponse
from django.views          import View
from django.db.models      import Q
from django.core.paginator import Paginator

from posts.models          import Post

class PostListView(View):
    def get(self, request):
        living_type = request.GET.get('living-type')
        room_size   = request.GET.get('room-size')
        family_type = request.GET.get('family-type')
        work_type   = request.GET.get('work-type')
        worker_type = request.GET.get('worker-type')
        limit       = int(request.GET.get("limit", 10))
        offset      = int(request.GET.get("offset", 1))

        queries = Q()

        if living_type:
            queries &= Q(living_type=living_type)
        
        if room_size:
            queries &= Q(room_size=room_size)

        if family_type:
            queries &= Q(family_type=family_type)

        if work_type:
            queries &= Q(work_type=work_type)

        if worker_type:
            queries &= Q(worker_type=worker_type)

        posts = Post.objects.filter(queries).order_by('-created_at').select_related('user').prefetch_related('photo_set')

        p = Paginator(posts, limit)
        pages_count = p.num_pages

        if offset < 1 or offset > pages_count:
            return JsonResponse({'result': 'INVALID_PAGE'}, status=404)

        total = {
            'total_items' : posts.count(),
            'total_pages' : pages_count,
            'current_page': offset,
            'limit'       : limit
        }
        
        page_items = p.page(offset) 
        posts = [{
            'id'               : page_item.id,
            'cover_image'      : page_item.cover_image,
            'first_description': page_item.photo_set.all()[0].description,
            'user' : {
                'id' : page_item.user.id,
                'nickname' : page_item.user.nickname
            }
        } for page_item in page_items]

        return JsonResponse({'total' : total, 'posts': posts}, status=200)

class PostItemView(View):
    def get(self, request, post_id):
        post = Post.objects\
            .select_related('user')\
            .prefetch_related('photo_set', 'photo_set__tag_set__product')\
            .get(id=1)
        
        result = {
            'user' : {
                'id'           : post.user.nickname,
                'profile_image': post.user.profile_image,
                'nickname'     : post.user.nickname
            },
            'post' : {
                'id'         : post.id,
                'contents' : [{
                    'photo_id'   : photo.id,
                    'description': photo.description,
                    'url'        : photo.url,
                    'tags' : [{
                        'point_x' : tag.point_x,
                        'point_y' : tag.point_y,
                        'product' : {
                            'id'   : tag.product.id,
                            'title': tag.product.title
                        }
                    } for tag in photo.tag_set.all()] 
                } for photo in post.photo_set.all()],
            }
        }

        return JsonResponse({'results': result}, status=200)

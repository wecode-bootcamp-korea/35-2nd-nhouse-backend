from django.http           import JsonResponse
from django.views          import View
from django.db.models      import Q
from django.core.paginator import Paginator
from django.db.models      import Count

from posts.models          import Post, User
from core.utils            import login_decorator

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
            'cover_image'      : page_item.photo_set.all()[0].url,
            'first_description': page_item.photo_set.all()[0].description,
            'user' : {
                'id'           : page_item.user.id,
                'nickname'     : page_item.user.nickname,
                'profile_image': page_item.user.profile_image
            }
        } for page_item in page_items]

        return JsonResponse({'total' : total, 'posts': posts}, status=200)

class PostItemView(View):
    def get(self, request, post_id):
        try: 
            post = Post.objects\
                .select_related('user')\
                .prefetch_related('photo_set', 'photo_set__tag_set__product')\
                .get(id=post_id)
            
            result = {
                'user' : {
                    'id'           : post.user.id,
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
                                'id'        : tag.product.id,
                                'title'     : tag.product.title,
                                'main_image': tag.product.main_image
                            }
                        } for tag in photo.tag_set.all()] 
                    } for photo in post.photo_set.all()],
                }
            }

            return JsonResponse({'results': result}, status=200)

        except Post.DoesNotExist:
                return JsonResponse({"message":"INVALID_POST"}, status=400)

class FollowListView(View):
    @login_decorator
    def get(self, request):
        limit       = int(request.GET.get("limit", 10))
        offset      = int(request.GET.get("offset", 1))
        followings  = request.user.followers.all()

        if followings:
            posts = Post.objects.filter(user__in = followings)\
                    .order_by('-created_at')\
                    .select_related('user')\
                    .prefetch_related('photo_set')

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
                'cover_image'      : page_item.photo_set.all()[0].url,
                'first_description': page_item.photo_set.all()[0].description,
                'user' : {
                    'id'           : page_item.user.id,
                    'nickname'     : page_item.user.nickname,
                    'profile_image': page_item.user.profile_image
                }
            } for page_item in page_items]

            return JsonResponse({'total' : total, 'posts': posts}, status=200)

        else:
            top_10_users = User.objects.all()\
                .prefetch_related('post_set__photo_set')\
                .annotate(follower_count=Count('followed_by'))\
                .order_by('-follower_count')[:10]
           
            result = [{
                'user' : {
                    'id'           : user.id,
                    'nickname'     : user.nickname,
                    'profile_image': user.profile_image
                },
                'posts' : [{
                    'id'         : post.id,
                    'cover_image': post.photo_set.all()[0].url
                } for post in user.post_set.all()[:4]]
            } for user in top_10_users]

            return JsonResponse({'result' : result}, status=200)




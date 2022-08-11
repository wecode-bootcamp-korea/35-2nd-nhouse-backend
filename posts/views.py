import json
import uuid
import boto3

from django.http           import JsonResponse
from django.views          import View
from django.db.models      import Q
from django.core.paginator import Paginator
from django.db.models      import Count
from django.db             import transaction

from posts.models          import Post, Photo, Tag, User
from nhouse.settings       import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY
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




class PostView(View):

    s3_client = boto3.client(
        's3',
        aws_access_key_id     = AWS_ACCESS_KEY_ID,
        aws_secret_access_key = AWS_SECRET_ACCESS_KEY
    )

    @login_decorator
    def post(self, request):
        try:
            data        = json.loads(request.POST.get('data'))
            user        = request.user
            living_type = data.get('living_type')
            room_size   = data.get('room_size')
            family_type = data.get('family_type')
            work_type   = data.get('work_type')
            description = data.get('contents_description')
            tags        = data.get('tag')
            filename    = request.FILES['filename']
            url         = str(uuid.uuid4())
            
            with transaction.atomic():
                post = Post.objects.create(
                    living_type = living_type,
                    room_size   = room_size,
                    family_type = family_type,
                    work_type   = work_type,
                    user        = user,
                    title       = 'none',
                    content     = 'none',
                    cover_image = 'none',
                    worker_type = 'none'
                )

                photo = Photo.objects.create(
                    post        = post,
                    description = description,
                    url         = "https://testnhousebucket.s3.ap-northeast-2.amazonaws.com/"+url,
                )
                
                for tag in tags:
                    Tag.objects.create(
                        point_x    = tag['point_x'],
                        point_y    = tag['point_y'],
                        photo      = photo,
                        product_id = tag['product_id']
                    )

            self.s3_client.upload_fileobj(
                filename, "testnhousebucket", url)

            return JsonResponse({"message":"SUCCESS"},status=200)

        except KeyError:
            return JsonResponse({"message":"KEYERROR"}, status = 400)
        except User.DoesNotExist:
            return JsonResponse({"message":"User Doesn Not Exist"}, status = 400)

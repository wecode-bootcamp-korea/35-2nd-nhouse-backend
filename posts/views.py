import json
import boto3
import uuid

from django.http           import JsonResponse
from django.views          import View
from django.db.models      import Q
from django.core.paginator import Paginator
from django.conf           import settings
from django.db             import transaction

from posts.models          import Post, Photo, Tag

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
        
class AWSFileUploader:
    def __init__(self, config):
        self.config = config
        self.client = boto3.resource(
            's3',
            aws_access_key_id     = self.config['access_key_id'],
            aws_secret_access_key = self.config['secret_access_key']
        )

    def upload(self, file):
        try:
            file._set_name(str(uuid.uuid4()))
            key = f'posts/{str(uuid.uuid4())}'  
            self.client.Bucket(self.config['bucket_name']).put_object(
                Key=key, Body=file, ContentType='jpeg')
            
            return self.config['image_url'] + key
            
        except: 
            return None

class FileHandler:
    def __init__(self, file_uploader):
        self.file_uploader = file_uploader 

    def upload(self, file):
        return self.file_uploader.upload(file)


class PostWriteView(View):
    def post(self, request):
        try:
            data        = json.loads(request.POST.get('data'))
            living_type = data.get('living_type')
            room_size   = data.get('room_size')
            family_type = data.get('family_type')
            work_type   = data.get('work_type')
            contents    = data.get('contents')
            files       = request.FILES.getlist('photo')
            user_id     = 1

            if len(files) != len(contents):
                return JsonResponse({'message':'INVALID_LENGTH'}, status=400)

            post = Post.objects.create(
                title       = 'fake title',
                content     = 'fake contents',
                cover_image = 'fake image url',
                living_type = living_type,
                room_size   = room_size,
                family_type = family_type,
                work_type   = work_type,
                worker_type = 'fake worker type',
                user_id     = user_id
            )

            file_uploader = AWSFileUploader(settings.AWS_CONFIG)
            file_handler = FileHandler(file_uploader)
            
            with transaction.atomic():
                for i in range(0, len(files)):
                    photo_url = file_handler.upload(files[i])
                    
                    if not photo_url:
                        return JsonResponse({'results': 'UPLOAD_FAILED'}, status=400)

                    current_content = contents[i]

                    photo = Photo.objects.create(
                        description = current_content['description'],
                        url         = photo_url,
                        post        = post
                    )
                    
                    tags = current_content.get('tags')
                    if tags:
                        for tag in tags:
                            Tag.objects.create(
                                point_x    = tag['point_x'],
                                point_y    = tag['point_y'],
                                photo      = photo,
                                product_id = tag['product_id']
                            )

            return JsonResponse({'results': 'SUCCESS'}, status=201)
        
        except KeyError:
            return JsonResponse({'message':'KEY_ERROR'}, status=400) 

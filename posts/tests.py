from django.test  import TestCase, Client

from posts.models import Post, Photo
from users.models import User

class PostListViewTest(TestCase):
    def setUp(self):
        User.objects.bulk_create([
            User(id=1, kakao_id = 1234)
        ])

        Post.objects.bulk_create([
            Post(
                id          = 1,
                title       = '트렌디한 인테리어 시공으로 살림이 즐거워지는 집',
                content     = '안녕하세요.',
                cover_image = 'https://images.unsplash.com/photo-1513694203232-719a280e022f?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1738&q=80',
                living_type = '원룸',
                room_size   = '10평 미만',
                family_type = '싱글라이프',
                work_type   = '홈스타일링',
                worker_type = '셀프',
                user_id     = 1 
            ),
            Post(
                id          = 2,
                title       = '트렌디한 인테리어 시공으로 살림이 즐거워지는 집',
                content     = '안녕하세요.',
                cover_image = 'https://images.unsplash.com/photo-1522771739844-6a9f6d5f14af?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1171&q=80',
                living_type = '오피스텔',
                room_size   = '10평대',
                family_type = '부부',
                work_type   = '리모델링',
                worker_type = '반셀프',
                user_id     = 1 
            )
        ])

        Photo.objects.bulk_create([
            Photo(
                id          = 1,
                description = '오늘, 우리집. 얼마만에 푹 쉬는 주말인지.',
                url         = 'https://images.unsplash.com/photo-1513694203232-719a280e022f?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1738&q=80',
                post_id     = 1
            ),
            Photo(
                id          = 2,
                description = '다채로운 꽃이 한가득 새겨진 쿠션커버',
                url         = 'https://images.unsplash.com/photo-1522771739844-6a9f6d5f14af?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1171&q=80',
                post_id     = 1
            ),
            Photo(
                id          = 3,
                description = '흐린 날, 간접 조명은 더욱 빛을 발한다.',
                url         = 'https://images.unsplash.com/photo-1522771739844-6a9f6d5f14af?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1171&q=80',
                post_id     = 2
            ),
            Photo(
                id          = 4,
                description = '너무 귀여운 아보카도 베딩',
                url         = 'https://images.unsplash.com/photo-1586023492125-27b2c045efd7?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=958&q=80',
                post_id     = 2
            )
        ])

    def tearDown(self):
        Post.objects.all().delete()
        User.objects.all().delete()
        Photo.objects.all().delete()

    def test_success_filter_all(self):
        client = Client()
        response = client.get('/posts/list?living-type=원룸&room-size=10평 미만&family-type=싱글라이프&work-type=홈스타일링&worker-type=셀프')
    
        self.assertEqual(response.json(),{
            "total": {
                "total_items": 1,
                "total_pages": 1,
                "current_page": 1,
                "limit": 10
            },
            "posts": [
                {
                    "id": 1,
                    "cover_image": "https://images.unsplash.com/photo-1513694203232-719a280e022f?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1738&q=80",
                    "first_description": "오늘, 우리집. 얼마만에 푹 쉬는 주말인지.",
                    "user": {
                        "id": 1,
                        "nickname": None
                    }
                }
            ]
        })

    def test_success_no_matching_queries(self):
        client = Client()
        response = client.get('/posts/list?living-type=오피스텔&room-size=10평 미만&family-type=싱글라이프&work-type=홈스타일링&worker-type=셀프')
        self.assertEqual(response.json(), {
            "total": {
                "total_items": 0,
                "total_pages": 1,
                "current_page": 1,
                "limit": 10
            },
            "posts": []
        })

    def test_fail_invalid_page(self):
        client = Client()
        response = client.get('/posts/list?offset=100')

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {'result': 'INVALID_PAGE'})
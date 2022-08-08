from django.test     import TestCase, Client 

from products.models import Product, Brand, FirstCategory, SecondCategory

class ProductsSearchViewTest(TestCase):
    def setUp(self):
        FirstCategory.objects.create(
            id   = 1,
            name = '가구',
        )

        SecondCategory.objects.create(
            id                = 1,
            name              = '침대',
            first_category_id = 1
        )

        Brand.objects.bulk_create([
            Brand(id=1, name="마틸라"),
            Brand(id=2, name="헬로우슬립"),
            Brand(id=3, name="픽켄드"),
            Brand(id=4, name="마이센스")
        ])

        Product.objects.bulk_create([
            Product(
                id                 = 1,
                title              = "클레어 수납침대",
                brand_id           = 1,
                main_image         = "http://images.com",
                second_category_id = 1,
                price              = 2000
            ),
            Product(
                id                 = 2,
                title              = "헤이나 멀티 수납침대",
                brand_id           = 2,
                main_image         = "http://images.com",
                second_category_id = 1,
                price              = 2000
            ),
            Product(
                id                 = 3,
                title              = "델루나 프리미엄 수납 호텔침대",
                brand_id           = 2,
                main_image         = "http://images.com",
                second_category_id = 1,
                price              = 2000
            ),
            Product(
                id                 = 4,
                title              = "헨트데이베드 고무나무 3인 패브릭 소파",
                brand_id           = 3,
                main_image         = "http://images.com",
                second_category_id = 1,
                price              = 2000
            ),
            Product(
                id                 = 5,
                title              = "프라제르 아쿠아텍스 4인용 소파",
                brand_id           = 4,
                main_image         = "http://images.com",
                second_category_id = 1,
                price              = 2000
            ),
            Product(
                id                 = 6,
                title              = "오굿즈 페브 아쿠아텍스 3인 소파",
                brand_id           = 1,
                main_image         = "http://images.com",
                second_category_id = 1,
                price              = 2000
            ),
            Product(
                id                 = 7,
                title              = "몽쉘 아쿠아텍스 조야 패브릭 2인 소파",
                brand_id           = 1,
                main_image         = "http://images.com",
                second_category_id = 1,
                price              = 2000
            ),
            Product(
                id                 = 8,
                title              = "JUSTINA 체어 패드 방석",
                brand_id           = 1,
                main_image         = "http://images.com",
                second_category_id = 1,
                price              = 2000
            )
        ])
        
    def tearDown(self):
        Product.objects.all().delete()
        SecondCategory.objects.all().delete()
        FirstCategory.objects.all().delete()
        Brand.objects.all().delete()
        
    def test_success_search_alphabet(self):
        client = Client()
        response = client.get('/search/products?keyword=ju', content_type='applications/json')
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {
            "total": {
                "total_items": 1,
                "total_pages": 1,
                "current_page": 1,
                "limit": 5
            },
            "result": [
                {
                    "id": 8,
                    "title": "JUSTINA 체어 패드 방석",
                    "main_image": "http://images.com",
                    "price": '2000.000',
                    "brand": "마틸라"
                }
            ]
        })
    
    def test_fail_invalid_offset_zero(self):
        client = Client()
        response = client.get('/search/products?offset=0', content_type='applications/json')
        
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {'result': 'INVALID_PAGE'})

   

    

    
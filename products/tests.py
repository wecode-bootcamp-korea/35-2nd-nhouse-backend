from django.test import TestCase, Client

from products.models import *

class ProductListViewTest(TestCase):
    def setUp(self):
        Brand.objects.bulk_create([Brand(id=1, name = 'data_brand1')])
        FirstCategory.objects.bulk_create([FirstCategory(id=1, name = 'data_first_category1')])
        SecondCategory.objects.bulk_create([
            SecondCategory(id=1, name = 'data_second_category1', first_category_id = 1),
            SecondCategory(id=2, name = 'data_second_category2', first_category_id = 1)])
        Product.objects.bulk_create([
            Product(
                id                 = 1,
                title              = 'data_test1',
                main_image         = 'https://pbs.twimg.com/media/FSYpcJkaAAAzLzw.jpg',
                price              = 100.000,
                brand_id           = 1,
                second_category_id = 1,
            ),
            Product(
                id                 = 2,
                title              = 'data_test2',
                main_image         = 'https://pbs.twimg.com/media/FSYpcJkaAAAzLzw.jpg',
                price              = 200.000,
                brand_id           = 1,
                second_category_id = 2,
            )
        ])

    def tearDown(self):
        Product.objects.all().delete()
        FirstCategory.objects.all().delete()
        SecondCategory.objects.all().delete()
        Brand.objects.all().delete()

    def test_success_all_products(self):
        client = Client()
        response = client.get('/products')
        self.assertEqual(response.json(), {
            "results": [{
                "product_id": 1,
                "title": "data_test1",
                "brand": "data_brand1",
                "price": "100.000",
                "first_category_id": 1,
                "second_category_id": 1,
                "main_image" : "https://pbs.twimg.com/media/FSYpcJkaAAAzLzw.jpg",
                },
                {
                "product_id": 2,
                "title": "data_test2",
                "brand": "data_brand1",
                "price": "200.000",
                "first_category_id": 1,
                "second_category_id": 2,
                "main_image" : "https://pbs.twimg.com/media/FSYpcJkaAAAzLzw.jpg",
                }],
                "exist_nest_page":False
        })
        self.assertEqual(response.status_code,200)

    def test_success_second_product(self):
        client = Client()
        response = client.get('/products?second_category=1')
        self.assertEqual(response.json(), {
            "results": [{
                "product_id": 1,
                "title": "data_test1",
                "brand": "data_brand1",
                "price": "100.000",
                "first_category_id": 1,
                "second_category_id": 1,
                "main_image" : "https://pbs.twimg.com/media/FSYpcJkaAAAzLzw.jpg",
                }],
            "exist_nest_page":False
        })
        self.assertEqual(response.status_code,200)
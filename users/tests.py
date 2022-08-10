from django.test import TestCase, Client
from unittest.mock import patch

from users.models import User, Follow 

class LoginViewTest(TestCase):
    def setUp(self):
        User.objects.create(
            id = 1,
            kakao_id = 12345,
            email = 'snoopy@gmail.com',
            nickname = 'Snoopy',
            profile_image = 'http://snoopy.com'
        )

    def tearDown(self):
        User.objects.all().delete()
    
    @patch('users.views.KakaoAPI.get_kakao_user_data')
    @patch('users.views.KakaoAPI.get_access_token')
    def test_success_login_with_same_nickname_email_profile_image(self, mocked_access_token, mocked_user_data):
        client = Client()

        mocked_access_token.return_value = '1234'
        mocked_user_data.return_value = {
                    'id': 12345, 
                    'kakao_account': {
                        'profile': {
                            'nickname': 'snoopy', 
                            'thumbnail_image_url': 'http://snoopy.com', 
                            'profile_image_url': 'http://snoopy.com'
                            }, 
                        'email': 'snoopy@gmail.com'
                        }
                    }

        header = {'HTTP_AUTHORIZATION' : '12341234'}
        response = client.get('/users/login', content_type='applications/json', **header)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json().get('message'), 'LOGIN_SUCCESS')

    @patch('users.views.KakaoAPI.get_kakao_user_data')
    @patch('users.views.KakaoAPI.get_access_token')
    def test_success_login_without_nickname_email_profile_image(self, mocked_access_token, mocked_user_data):
        client = Client()

        mocked_access_token.return_value = '1234'
        mocked_user_data.return_value = {
            'id': 12345, 
            'kakao_account': {
                'profile_nickname_needs_agreement': False, 
                'profile_image_needs_agreement': False, 
                'has_email': True, 
                'email_needs_agreement': True
                }
            }

        header = {'HTTP_AUTHORIZATION' : '12341234'}
        response = client.get('/users/login', content_type='applications/json', **header)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json().get('message'), 'LOGIN_SUCCESS') 

    @patch('users.views.KakaoAPI.get_kakao_user_data')
    @patch('users.views.KakaoAPI.get_access_token')
    def test_success_login_with_different_nickname(self, mocked_access_token, mocked_user_data):
        client = Client()

        mocked_access_token.return_value = '1234'
        mocked_user_data.return_value = {
            'id': 12345, 
            'kakao_account': {
                'profile': {
                    'nickname': 'snoopy12', 
                    'profile_image_url': 'http://snoopy.com'
                    }, 
                'email': 'snoopy@gmail.com'
                }
            }

        header = {'HTTP_AUTHORIZATION' : '12341234'}
        response = client.get('/users/login', content_type='applications/json', **header)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json().get('message'), 'LOGIN_SUCCESS') 
        self.assertEqual(User.objects.get(id=1).nickname, 'snoopy12')

    @patch('users.views.KakaoAPI.get_kakao_user_data')
    @patch('users.views.KakaoAPI.get_access_token')
    def test_success_login_with_different_profile_image(self, mocked_access_token, mocked_user_data):
        client = Client()

        mocked_access_token.return_value = '1234'
        mocked_user_data.return_value = {
            'id': 12345, 
            'kakao_account': {
                'profile': {
                    'nickname': 'snoopy', 
                    'profile_image_url': 'http://snoopy12.com'
                    }, 
                'email': 'snoopy@gmail.com'
                }
            }

        header = {'HTTP_AUTHORIZATION' : '12341234'}
        response = client.get('/users/login', content_type='applications/json', **header)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json().get('message'), 'LOGIN_SUCCESS') 
        self.assertEqual(User.objects.get(id=1).profile_image, 'http://snoopy12.com')

    @patch('users.views.KakaoAPI.get_kakao_user_data')
    @patch('users.views.KakaoAPI.get_access_token')
    def test_success_login_with_different_email(self, mocked_access_token, mocked_user_data):
        client = Client()

        mocked_access_token.return_value = '1234'
        mocked_user_data.return_value = {
            'id': 12345, 
            'kakao_account': {
                'profile': {
                    'nickname': 'snoopy', 
                    'profile_image_url': 'http://snoopy.com'
                    }, 
                'email': 'snoopy12@gmail.com'
                }
            }

        header = {'HTTP_AUTHORIZATION' : '12341234'}
        response = client.get('/users/login', content_type='applications/json', **header)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json().get('message'), 'LOGIN_SUCCESS') 
        self.assertEqual(User.objects.get(id=1).email, 'snoopy12@gmail.com') 

    @patch('users.views.KakaoAPI.get_kakao_user_data')
    @patch('users.views.KakaoAPI.get_access_token')
    def test_success_signup_with_nickname_email_profile_image(self, mocked_access_token, mocked_user_data):
        client = Client()

        mocked_access_token.return_value = '1234'
        mocked_user_data.return_value = {
            'id': 678910, 
            'kakao_account': {
                'profile': {
                    'nickname': 'garfield', 
                    'profile_image_url': 'http://garfield.com'
                    }, 
                'email': 'garfield@gmail.com'
                }
            }

        header = {'HTTP_AUTHORIZATION' : '12341234'}
        response = client.get('/users/login', content_type='applications/json', **header)
        
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json().get('message'), 'SIGNUP_SUCCESS') 

    @patch('users.views.KakaoAPI.get_kakao_user_data')
    @patch('users.views.KakaoAPI.get_access_token')
    def test_success_signup_without_nickname_email_profile_image(self, mocked_access_token, mocked_user_data):
        client = Client()

        mocked_access_token.return_value = '1234'
        mocked_user_data.return_value = {
            'id': 678910, 
            'kakao_account': {
                'profile_nickname_needs_agreement': False, 
                'profile_image_needs_agreement': False, 
                'has_email': True, 
                'email_needs_agreement': True
                }
            }

        header = {'HTTP_AUTHORIZATION' : '12341234'}
        response = client.get('/users/login', content_type='applications/json', **header)
        
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json().get('message'), 'SIGNUP_SUCCESS') 

    @patch('users.views.KakaoAPI.get_kakao_user_data')
    @patch('users.views.KakaoAPI.get_access_token')
    def test_success_signup_without_nickname(self, mocked_access_token, mocked_user_data):
        client = Client()

        mocked_access_token.return_value = '1234'
        mocked_user_data.return_value = {
            'id': 678910, 
            'kakao_account': {
                'profile': {
                    'profile_image_url': 'http://garfield.com'
                    }, 
                'email': 'garfield@gmail.com'
                }
            }

        header = {'HTTP_AUTHORIZATION' : '12341234'}
        response = client.get('/users/login', content_type='applications/json', **header)
        
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json().get('message'), 'SIGNUP_SUCCESS')  

    @patch('users.views.KakaoAPI.get_kakao_user_data')
    @patch('users.views.KakaoAPI.get_access_token')
    def test_success_signup_without_profile_image(self, mocked_access_token, mocked_user_data):
        client = Client()

        mocked_access_token.return_value = '1234'
        mocked_user_data.return_value = {
            'id': 678910, 
            'kakao_account': {
                'profile': {
                    'nickname': 'garfield'
                    }, 
                'email': 'garfield@gmail.com'
                }
            }

        header = {'HTTP_AUTHORIZATION' : '12341234'}
        response = client.get('/users/login', content_type='applications/json', **header)
        
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json().get('message'), 'SIGNUP_SUCCESS') 

    @patch('users.views.KakaoAPI.get_kakao_user_data')
    @patch('users.views.KakaoAPI.get_access_token')
    def test_success_signup_without_email(self, mocked_access_token, mocked_user_data):
        client = Client()

        mocked_access_token.return_value = '1234'
        mocked_user_data.return_value = {
            'id': 678910, 
            'kakao_account': {
                'profile': {
                    'nickname': 'garfield', 
                    'profile_image_url': 'http://garfield.com'
                    }
                }
            }

        header = {'HTTP_AUTHORIZATION' : '12341234'}
        response = client.get('/users/login', content_type='applications/json', **header)
        
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json().get('message'), 'SIGNUP_SUCCESS')  

    @patch('users.views.KakaoAPI.get_kakao_user_data')
    @patch('users.views.KakaoAPI.get_access_token')
    def test_fail_invalid_authorization_code(self, mocked_access_token, mocked_user_data):
        client = Client()

        mocked_access_token.return_value = '1234'
        mocked_user_data.return_value = {
            'id': 678910, 
            'kakao_account': {
                'profile': {
                    'nickname': 'garfield', 
                    'profile_image_url': 'http://garfield.com'
                    }, 
                'email': 'garfield@gmail.com'
                }
            }

        header = {'HTTP_AUTHORIZATION' : ''}
        response = client.get('/users/login', content_type='applications/json', **header)
        
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json().get('message'), "INVALID_AUTHORIZATION_CODE") 

    @patch('users.views.KakaoAPI.get_kakao_user_data')
    @patch('users.views.KakaoAPI.get_access_token')
    def test_fail_invalid_access_token(self, mocked_access_token, mocked_user_data):
        client = Client()

        mocked_access_token.return_value = ''
        mocked_user_data.return_value = {
            'id': 678910, 
            'kakao_account': {
                'profile': {
                    'nickname': 'garfield', 
                    'profile_image_url': 'http://garfield.com'
                    }, 
                'email': 'garfield@gmail.com'
                }
            }

        header = {'HTTP_AUTHORIZATION' : '12341234'}
        response = client.get('/users/login', content_type='applications/json', **header)

        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json().get('message'), "INVALID_ACCESS_TOKEN") 

    @patch('users.views.KakaoAPI.get_kakao_user_data')
    @patch('users.views.KakaoAPI.get_access_token')
    def test_fail_invalid_kakao_id(self, mocked_access_token, mocked_user_data):
        client = Client()

        mocked_access_token.return_value = '1234'
        mocked_user_data.return_value = {}

        header = {'HTTP_AUTHORIZATION' : '12341234'}
        response = client.get('/users/login', content_type='applications/json', **header)
        
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json().get('message'), 'INVALID_KAKAO_ID') 



    
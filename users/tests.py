from django.test import TestCase, Client
from unittest.mock import patch, MagicMock

from users.models import User, Follow 

class LoginViewTestSetting(TestCase):
    def execute(self, mocked_request, MockedAccessToken, MockedUserData, authorization_code, status_code, response_message):
        client = Client()
        mock = MagicMock()
        mock.side_effect = [MockedAccessToken, MockedUserData]
        mocked_request.post = mock
        
        header = {'HTTP_AUTHORIZATION' : authorization_code}
        response = client.get('/users/login', content_type='applications/json', **header)
        
        self.assertEqual(response.status_code, status_code)
        self.assertEqual(response.json().get('message'), response_message)

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

    @patch('users.views.requests')
    def test_success_login_with_same_nickname_email_profile_image(self, mocked_request):
        class MockedAccessToken:
            def json(self):
                return {'access_token' : '1234'}

        class MockedUserData:
            def json(self):
                return {
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

        authorization_code = '12341234'
        status_code = 200
        response_message = 'LOGIN_SUCCESS'

        test = LoginViewTestSetting()
        test.execute(mocked_request, MockedAccessToken(), MockedUserData(), authorization_code, status_code, response_message)
    
    @patch('users.views.requests')
    def test_success_login_without_nickname_email_profile_image(self, mocked_request):
        class MockedAccessToken:
            def json(self):
                return {'access_token' : '1234'}

        class MockedUserData:
            def json(self):
                return {
                    'id': 12345, 
                    'kakao_account': {
                        'profile_nickname_needs_agreement': False, 
                        'profile_image_needs_agreement': False, 
                        'has_email': True, 
                        'email_needs_agreement': True
                        }
                    }   
        authorization_code = '12341234'
        status_code = 200
        response_message = 'LOGIN_SUCCESS'

        test = LoginViewTestSetting()
        test.execute(mocked_request, MockedAccessToken(), MockedUserData(), authorization_code, status_code, response_message)

    @patch('users.views.requests')
    def test_success_login_with_different_nickname(self, mocked_request):
        class MockedAccessToken:
            def json(self):
                return {'access_token' : '1234'}

        class MockedUserData:
            def json(self):
                return {
                    'id': 12345, 
                    'kakao_account': {
                        'profile': {
                            'nickname': 'snoopy12', 
                            'profile_image_url': 'http://snoopy.com'
                            }, 
                        'email': 'snoopy@gmail.com'
                        }
                    }

        authorization_code = '12341234'
        status_code = 200
        response_message = 'LOGIN_SUCCESS'

        test = LoginViewTestSetting()
        test.execute(mocked_request, MockedAccessToken(), MockedUserData(), authorization_code, status_code, response_message)

    @patch('users.views.requests')
    def test_success_login_with_different_profile_image(self, mocked_request):
        class MockedAccessToken:
            def json(self):
                return {'access_token' : '1234'}

        class MockedUserData:
            def json(self):
                return {
                    'id': 12345, 
                    'kakao_account': {
                        'profile': {
                            'nickname': 'snoopy', 
                            'profile_image_url': 'http://snoopy111.com'
                            }, 
                        'email': 'snoopy@gmail.com'
                        }
                    }

        authorization_code = '12341234'
        status_code = 200
        response_message = 'LOGIN_SUCCESS'

        test = LoginViewTestSetting()
        test.execute(mocked_request, MockedAccessToken(), MockedUserData(), authorization_code, status_code, response_message)

    @patch('users.views.requests')
    def test_success_login_with_different_email(self, mocked_request):
        class MockedAccessToken:
            def json(self):
                return {'access_token' : '1234'}

        class MockedUserData:
            def json(self):
                return {
                    'id': 12345, 
                    'kakao_account': {
                        'profile': {
                            'nickname': 'snoopy', 
                            'profile_image_url': 'http://snoopy.com'
                            }, 
                        'email': 'snoopy123@gmail.com'
                        }
                    }

        authorization_code = '12341234'
        status_code = 200
        response_message = 'LOGIN_SUCCESS'

        test = LoginViewTestSetting()
        test.execute(mocked_request, MockedAccessToken(), MockedUserData(), authorization_code, status_code, response_message)

    @patch('users.views.requests')
    def test_success_signup_with_nickname_email_profile_image(self, mocked_request):
        class MockedAccessToken:
            def json(self):
                return {'access_token' : '1234'}

        class MockedUserData:
            def json(self):
                return {
                    'id': 678910, 
                    'kakao_account': {
                        'profile': {
                            'nickname': 'garfield', 
                            'profile_image_url': 'http://garfield.com'
                            }, 
                        'email': 'garfield@gmail.com'
                        }
                    }  
        authorization_code = '12341234'
        status_code = 201
        response_message = 'SIGNUP_SUCCESS'

        test = LoginViewTestSetting()
        test.execute(mocked_request, MockedAccessToken(), MockedUserData(), authorization_code, status_code, response_message)

    @patch('users.views.requests')
    def test_success_signup_without_nickname_email_profile_image(self, mocked_request):
        class MockedAccessToken:
            def json(self):
                return {'access_token' : '1234'}

        class MockedUserData:
            def json(self):
                return {
                    'id': 678910, 
                    'kakao_account': {
                        'profile_nickname_needs_agreement': False, 
                        'profile_image_needs_agreement': False, 
                        'has_email': True, 
                        'email_needs_agreement': True
                        }
                    }   
        authorization_code = '12341234'
        status_code = 201
        response_message = 'SIGNUP_SUCCESS'

        test = LoginViewTestSetting()
        test.execute(mocked_request, MockedAccessToken(), MockedUserData(), authorization_code, status_code, response_message)

    @patch('users.views.requests')
    def test_success_signup_without_nickname(self, mocked_request):
        class MockedAccessToken:
            def json(self):
                return {'access_token' : '1234'}

        class MockedUserData:
            def json(self):
                return {
                    'id': 678910, 
                    'kakao_account': {
                        'profile': {
                            'profile_image_url': 'http://garfield.com'
                            }, 
                        'email': 'garfield@gmail.com'
                        }
                    } 
        authorization_code = '12341234'
        status_code = 201
        response_message = 'SIGNUP_SUCCESS'

        test = LoginViewTestSetting()
        test.execute(mocked_request, MockedAccessToken(), MockedUserData(), authorization_code, status_code, response_message)

    @patch('users.views.requests')
    def test_success_signup_without_profile_image(self, mocked_request):
        class MockedAccessToken:
            def json(self):
                return {'access_token' : '1234'}

        class MockedUserData:
            def json(self):
                return {
                    'id': 678910, 
                    'kakao_account': {
                        'profile': {
                            'nickname': 'garfield'
                            }, 
                        'email': 'garfield@gmail.com'
                        }
                    } 
        authorization_code = '12341234'
        status_code = 201
        response_message = 'SIGNUP_SUCCESS'

        test = LoginViewTestSetting()
        test.execute(mocked_request, MockedAccessToken(), MockedUserData(), authorization_code, status_code, response_message)

    @patch('users.views.requests')
    def test_success_signup_without_email(self, mocked_request):
        class MockedAccessToken:
            def json(self):
                return {'access_token' : '1234'}

        class MockedUserData:
            def json(self):
                return {
                    'id': 678910, 
                    'kakao_account': {
                        'profile': {
                            'nickname': 'garfield',
                            'profile_image_url': 'http://garfield.com'
                            }, 
                        }
                    } 
        authorization_code = '12341234'
        status_code = 201
        response_message = 'SIGNUP_SUCCESS'

        test = LoginViewTestSetting()
        test.execute(mocked_request, MockedAccessToken(), MockedUserData(), authorization_code, status_code, response_message)
    
    @patch('users.views.requests')
    def test_fail_invalid_authorization_code(self, mocked_request):
        class MockedAccessToken:
            def json(self):
                return {'access_token' : '1234'}

        class MockedUserData:
            def json(self):
                return {
                    'id': 12345, 
                    'kakao_account': {
                        'profile': {
                            'nickname': 'snoopy', 
                            'profile_image_url': 'http://snoopy.com'
                            }, 
                        'email': 'snoopy@gmail.com'
                        }
                    }

        authorization_code = ''
        status_code = 401
        response_message = "INVALID_AUTHORIZATION_CODE"

        test = LoginViewTestSetting()
        test.execute(mocked_request, MockedAccessToken(), MockedUserData(), authorization_code, status_code, response_message)
        
    @patch('users.views.requests')
    def test_fail_invalid_access_token(self, mocked_request):
        class MockedAccessToken:
            def json(self):
                return {'access_token' : ''}

        class MockedUserData:
            def json(self):
                return {
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

        authorization_code = '12341234'
        status_code = 401
        response_message = "INVALID_ACCESS_TOKEN"

        test = LoginViewTestSetting()
        test.execute(mocked_request, MockedAccessToken(), MockedUserData(), authorization_code, status_code, response_message)

    @patch('users.views.requests')
    def test_fail_invalid_kakao_id(self, mocked_request):
        class MockedAccessToken:
            def json(self):
                return {'access_token' : '1234'}

        class MockedUserData:
            def json(self):
                return {}

        authorization_code = '12341234'
        status_code = 401
        response_message = "INVALID_KAKAO_ID"

        test = LoginViewTestSetting()
        test.execute(mocked_request, MockedAccessToken(), MockedUserData(), authorization_code, status_code, response_message)
    
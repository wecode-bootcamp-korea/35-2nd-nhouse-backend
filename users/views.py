import jwt
import requests

from django.http      import JsonResponse
from django.views     import View
from django.conf      import settings

from users.models     import User

class LoginView(View):
    def get(self, request):
        try:
            code = request.META.get('HTTP_AUTHORIZATION')
            
            if not code:
                return JsonResponse({"message" : "INVALID_AUTHORIZATION_CODE"}, status=401)

            data = {
                'grant_type' : 'authorization_code',
                'client_id' : settings.KAKAO_REST_API_KEY,
                'redirect_uri' : settings.REDIRECT_URI,
                'code' : code
            }
            token_response = requests.post("https://kauth.kakao.com/oauth/token", data=data).json()
            access_token   = token_response.get('access_token')
          
            if not access_token:
                return JsonResponse({"message" : "INVALID_ACCESS_TOKEN"}, status=401)

            headers = {
                'Authorization': f'Bearer {access_token}'
            }
            user_data_response = requests.post("https://kapi.kakao.com/v2/user/me", headers=headers).json()
            kakao_id = user_data_response.get('id')
            
            if not kakao_id:
                return JsonResponse({"message" : "INVALID_KAKAO_ID"}, status=401)

            kakao_account = user_data_response['kakao_account']
            email         = kakao_account.get('email')
            nickname      = None 
            profile_image = None
            profile       = kakao_account.get('profile')

            if profile:
                nickname      = profile.get('nickname')
                profile_image = profile.get('profile_image_url')
                
            user, is_created = User.objects.get_or_create(
                kakao_id = kakao_id,
                defaults = {
                    "email"        : email,
                    "nickname"     : nickname,
                    "profile_image": profile_image
                }
            )
            nhouse_token = jwt.encode({"user_id" : user.id}, settings.SECRET_KEY, settings.ALGORITHM)

            if not is_created:
                if not user.email == email:
                    user.email = email 
                    user.save()
                if not user.profile_image == profile_image:
                    user.profile_image = profile_image
                    user.save()
                if not user.nickname == nickname:
                    user.nickname = nickname
                return JsonResponse({"message" : "LOGIN_SUCCESS", "access_token" : nhouse_token}, status=200)

            return JsonResponse({"message" : "SIGNUP_SUCCESS", "access_token" : nhouse_token}, status=201)  

        except KeyError:
            return JsonResponse({"message":"KEY_ERROR"}, status=400)

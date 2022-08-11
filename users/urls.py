from django.urls import path

from users.views import LoginView, FollowView

urlpatterns = [
    path('/login', LoginView.as_view()),
    path('/follow', FollowView.as_view())
]
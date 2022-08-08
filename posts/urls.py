from django.urls import path

from posts.views import PostListView

urlpatterns = [
    path('/list', PostListView.as_view()),
]
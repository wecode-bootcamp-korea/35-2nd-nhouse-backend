from django.urls import path

from posts.views import PostListView, PostItemView, FollowListView, PostView

urlpatterns = [
    path('/list', PostListView.as_view()),
    path('/<int:post_id>', PostItemView.as_view()),
    path('/follow', FollowListView.as_view()),
    path('', PostView.as_view()),
]
from django.urls import path

from posts.views import PostListView, PostItemView

urlpatterns = [
    path('/list', PostListView.as_view()),
    path('/<int:post_id>', PostItemView.as_view()),
]
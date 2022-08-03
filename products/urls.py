from django.urls import path

from products.views import FirstCategoryView

urlpatterns = [
    path('/category', FirstCategoryView.as_view()),
]
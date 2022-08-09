from django.urls import path

from products.views import FirstCategoryView,ProductDetailView

urlpatterns = [
    path('/category', FirstCategoryView.as_view()),
    path('/<int:product_id>', ProductDetailView.as_view()),
]

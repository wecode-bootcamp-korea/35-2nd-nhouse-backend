from django.urls import path

from products.views import FirstCategoryView,ProductDetailView, ProductListView

urlpatterns = [
    path('/category', FirstCategoryView.as_view()),
    path('/<int:product_id>', ProductDetailView.as_view()),
    path('', ProductListView.as_view()),
]
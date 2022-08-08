from django.urls import path

from search.views import ProductSearchView

urlpatterns = [
    path('/products', ProductSearchView.as_view()),
]
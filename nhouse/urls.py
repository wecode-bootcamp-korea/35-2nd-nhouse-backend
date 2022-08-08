from django.urls import path,include

urlpatterns = [
    path('products', include('products.urls')),
    path('users', include('users.urls')),
    path('search', include('search.urls')),
]

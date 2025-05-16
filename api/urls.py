
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *


urlpatterns = [
    path("Dang_ky/",RegisterSerializerView.as_view(), name="register"),
    path("Dang_nhap/",LoginSerializerView.as_view(), name="Login"),
    path("ResetPassWord/",ResetPassWordSerializerView.as_view(), name="ResetPassWord"),
    path('categories/', CategoryList.as_view(), name='category-list'),
    path('categories/<int:pk>/', CategoryDetail.as_view(), name='category-detail'),
    path('Product/<int:pk>/', ProductDetail.as_view(), name='product-detail'),
    path('Product/', ProductView.as_view(), name='Product'),
]
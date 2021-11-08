from . import views
from django.urls import path, re_path

urlpatterns = [
    path('private/', views.PostList.as_view(), name='private'),
    path('', views.PublicPostList.as_view(), name='home'),
    path('login/', views.CustomLogin.as_view(), name='custom_login'),
    path('<slug:slug>/', views.PublicPostDetail.as_view(), name='post_detail'),
    path('private/<slug:slug>/', views.PostDetail.as_view(), name='private_post_detail'),
]
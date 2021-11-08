from . import views
from django.urls import path, re_path

urlpatterns = [
    path('', views.index, name='new_post'),
    path('edit/', views.index, name='basic_post'),
    path('<slug:slug>/', views.edit_post, name='edit_post')
]
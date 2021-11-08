from . import views
from django.urls import path, re_path

urlpatterns = [
    path('', views.index, name='tracking'),
    path('graph', views.graph, name='graph')
]

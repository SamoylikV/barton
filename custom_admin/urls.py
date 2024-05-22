from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('labels/create/', views.create_label, name='create_label'),
    path('labels/update/<str:name>/', views.update_label, name='update_label'),
    path('labels/delete/<str:name>/', views.delete_label, name='delete_label'),
    path('labels/<str:name>/', views.label_detail, name='label_detail'),
    path('labels/', views.label_list, name='label_list'),
]
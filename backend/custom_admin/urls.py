from django.urls import path
from . import views

urlpatterns = [
    path('labels/create/', views.create_label, name='create_label'),
    path('labels/update/<str:name>/', views.update_label, name='update_label'),
    path('labels/delete/<str:name>/', views.delete_label, name='delete_label'),
    path('labels/<str:name>/', views.label_detail, name='label_detail'),
    path('labels/', views.label_list, name='label_list'),
    path('chats/', views.chat_list, name='chat_list'),
    path('chats/create/', views.create_chat, name='create_chat'),
    path('chats/<int:pk>/edit/', views.update_chat, name='update_chat'),
    path('chats/<int:pk>/delete/', views.delete_chat, name='delete_chat'),
    path('events/', views.event_list, name='event_list'),
    path('events/create/', views.create_event, name='create_event'),
    path('events/<int:pk>/edit/', views.update_event, name='update_event'),
    path('events/<int:pk>/delete/', views.delete_event, name='delete_event'),
    path('messages/', views.message_list, name='message_list'),
    path('messages/create/', views.create_message, name='create_message'),
    path('messages/update/<int:pk>/', views.update_message, name='update_message'),
    path('messages/delete/<int:pk>/', views.delete_message, name='delete_message'),
    path('metrics/', views.metrics_list, name='metrics_list'),
    path('', views.dashboard, name='dashboard'),
]
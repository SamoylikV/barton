from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/create/', views.create_user, name='create_user'),
    path('users/update/<str:tg_id>/', views.update_user, name='update_user'),
    path('users/delete/<str:tg_id>/', views.delete_user, name='delete_user'),
    path('users/<str:tg_id>/', views.user_detail, name='user_detail'),
    path('users/', views.user_list, name='user_list'),
    path('labels/<str:name>/', views.get_label_text, name='labels'),
    path('labels/all/', views.get_all_labels, name='all_labels'),
    # path('chats/', views.chat_list, name='chat_list'),
    # path('chats/create/', views.create_chat, name='create_chat'),
    # path('chats/<int:pk>/edit/', views.update_chat, name='update_chat'),
    # path('chats/<int:pk>/delete/', views.delete_chat, name='delete_chat'),
    # path('events/', views.event_list, name='event_list'),
    # path('events/create/', views.create_event, name='create_event'),
    # path('events/<int:pk>/edit/', views.update_event, name='update_event'),
    # path('events/<int:pk>/delete/', views.delete_event, name='delete_event'),
    path('', include('custom_admin.urls')),
]
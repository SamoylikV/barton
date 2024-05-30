from django.contrib import admin
from django.urls import path, include
from . import views
from custom_admin.views import create_label, update_label, delete_label, create_message, update_message, delete_message, message_list, metrics_list
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/create/', views.create_user, name='create_user'),
    path('users/update/<str:tg_id>/', views.update_user, name='update_user'),
    path('users/delete/<str:tg_id>/', views.delete_user, name='delete_user'),
    path('users/<str:tg_id>/', views.user_detail, name='user_detail'),
    path('users/', views.user_list, name='user_list'),
    path('labels/create/', create_label, name='create_label'),
    path('labels/update/<str:name>/', update_label, name='update_label'),
    path('labels/delete/<str:name>/', delete_label, name='delete_label'),
    path('labels/<str:name>/', views.get_label_text, name='labels'),
    path('labels/all/', views.get_all_labels, name='all_labels'),
    path('messages/', message_list, name='message_list'),
    path('messages/create/', create_message, name='create_message'),
    path('messages/update/<int:pk>/', update_message, name='update_message'),
    path('messages/delete/<int:pk>/', delete_message, name='delete_message'),
    path('metrics/', metrics_list, name='metrics_list'),
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

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
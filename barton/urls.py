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
    path('labels/', views.get_label_text, name='labels'),
    path('admin_panel/', include('custom_admin.urls'))
]
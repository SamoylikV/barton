from django.contrib import admin
from api.models import User, Labels, Chats, Events

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('tg_id', 'email', 'number', 'name', 'surname', 'subscription_signup_date', 'subscription_expiration')
    search_fields = ('tg_id', 'email', 'number', 'name', 'surname')

@admin.register(Labels)
class LabelsAdmin(admin.ModelAdmin):
    list_display = ('name', 'text', 'tag')
    search_fields = ('name', 'text')
    
    
@admin.register(Chats)
class ChatAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)

@admin.register(Events)
class EventAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'date')
    search_fields = ('name',)
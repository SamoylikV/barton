from django.contrib import admin
from barton.models import User, Labels

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('tg_id', 'email', 'number', 'name', 'surname', 'subscription_signup_date', 'subscription_expiration')
    search_fields = ('tg_id', 'email', 'number', 'name', 'surname')

@admin.register(Labels)
class LabelsAdmin(admin.ModelAdmin):
    list_display = ('name', 'text', 'tag')
    search_fields = ('name', 'text')
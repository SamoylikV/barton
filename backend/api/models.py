from django.db import models
from django.utils import timezone

class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    tg_id = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True, blank=True, null=True)
    number = models.CharField(max_length=15, unique=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    surname = models.CharField(max_length=100, blank=True, null=True)
    subscription_signup_date = models.DateTimeField(blank=True, null=True)
    subscription_expiration = models.DateTimeField(blank=True, null=True)
 
    def has_subscription_expired(self):
        return self.subscription_expiration and self.subscription_expiration < timezone.now()
    
    def __str__(self):
        return self.email

class Labels(models.Model):
    TAG_CHOICES = [
        ('start', 'старт'),
        ('greeting', 'приветствие'),
        ('data_collection', 'сбор данных'),
        ('menu', 'меню'),
        ('other', 'другое'),
    ]
    label_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    text = models.TextField(blank=True)
    tag = models.CharField(max_length=20, choices=TAG_CHOICES, default='other')

    def __str__(self):
        return self.name

class Events(models.Model):
    name = models.CharField(max_length=100)
    text = models.TextField(blank=True)
    date = models.DateTimeField()

    def __str__(self):
        return self.name

class Chats(models.Model):
    name = models.CharField(max_length=100)
    link = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Receipts(models.Model):
    name = models.CharField(max_length=100)
    link = models.CharField(max_length=100)
    tg_id = models.CharField(max_length=100)

    def __str__(self):
        return self.name
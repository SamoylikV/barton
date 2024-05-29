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
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    text = models.TextField(blank=True)
    tag = models.CharField(max_length=20, choices=TAG_CHOICES, default='other')

    def __init__(self, *args, **kwargs):
        super(Labels, self).__init__(*args, **kwargs)
        if not self.id:
            self.text = "_"
 
    def __str__(self):
        return self.name

    def delete(self, *args, **kwargs):
        if self.name in ['give_number', 'error', 'name', 'surname', 'email', 'thanks', 'get_link', 'menu', 'platform', 'back', 'declined']:
            return
        super(Labels, self).delete(*args, **kwargs)

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
    
class Groups(models.Model):
    chat_id = models.CharField(max_length=100, unique=True)
    
    def __str__(self):
        return self.chat_id
    
class Messages(models.Model):
    text = models.TextField(blank=True)
    date = models.DateTimeField()
    repeated = models.BooleanField(default=False)
    day_of_week = models.CharField(
        max_length=9,
        choices=[
            ('Monday', 'Monday'),
            ('Tuesday', 'Tuesday'),
            ('Wednesday', 'Wednesday'),
            ('Thursday', 'Thursday'),
            ('Friday', 'Friday'),
            ('Saturday', 'Saturday'),
            ('Sunday', 'Sunday'),
        ],
        blank=True,
        null=True
    )
    image = models.ImageField(upload_to='message_images/', blank=True, null=True)

    def __str__(self):
        return f"Message to be sent on {self.date} - Repeated: {self.repeated}"

    def save(self, *args, **kwargs):
        if not self.repeated:
            self.day_of_week = None
        super().save(*args, **kwargs)
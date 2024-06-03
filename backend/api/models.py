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
 
    def __str__(self):
        return self.name

    def delete(self, *args, **kwargs):
        if self.name in [
            'give_number', 'error', 'name', 'surname', 'email', 
            'thanks', 'get_link', 'menu', 'platform', 'back', 'declined',
            'next', 'all_done', 'choose_tier', 'tier_1', 'tier_2', 
            'free_help', 'club_discount', 'neuro_mark', 'nearest_events'
        ]:
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
    deal_id = models.CharField(max_length=100, blank=True)
    deal_number = models.CharField(max_length=100, blank=True)
    tg_id = models.CharField(max_length=100)
    tier = models.CharField(max_length=100, blank=True)
    payed = models.BooleanField(default=False)
    def __str__(self):
        return self.name
    
class Groups(models.Model):
    chat_id = models.CharField(max_length=100, unique=True)
    
    def __str__(self):
        return self.chat_id
    
class Messages(models.Model):
    text = models.TextField(blank=True)
    date = models.DateTimeField(blank=True, null=True)
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
    send_now = models.BooleanField(default=False)

    def __str__(self):
        return f"Сообщение: {self.text} - Дата: {self.date} - Повторять: {self.repeated}"

    def clean(self):
        if self.send_now and (self.date or self.day_of_week):
            raise Exception('Нельзя указывать дату при рассылке сейчас')
        if not self.send_now and not self.date:
            raise Exception('Нету даты для рассылки')

    def save(self, *args, **kwargs):
        if self.send_now:
            self.date = timezone.now()
            self.day_of_week = None
        elif not self.repeated:
            self.day_of_week = None
        super().save(*args, **kwargs)
        

class Metrics(models.Model):
    id = models.AutoField(primary_key=True)
    tg_id = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    spent = models.IntegerField(default=0)
    registration_date = models.DateTimeField(auto_now_add=True)
    month_since_join = models.IntegerField(default=0)
    
    def __str__(self):
        return self.name

    def update_metrics(self):
        self.month_since_join = self.calculate_months_since_join()
        self.save()

    def calculate_months_since_join(self):
        return (timezone.now() - self.registration_date).days // 30
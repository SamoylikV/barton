from django.db.models.signals import post_save, post_migrate
from django.dispatch import receiver
from .models import Labels, Metrics, User, Receipts
from django.utils import timezone
import json
import os
def get_cache_file_path():
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../tg_bot/label_cache.json')

def update_label_cache():
    labels = {label.name: label.text for label in Labels.objects.all()}
    cache_file_path = get_cache_file_path()
    with open(cache_file_path, 'w') as cache_file:
        json.dump(labels, cache_file)

@receiver(post_save, sender=Labels)
def update_label_cache_signal(sender, instance, **kwargs):
    update_label_cache()
    
@receiver(post_save, sender=User)
def create_or_update_metrics(sender, instance, **kwargs):
    if instance.name:
        metrics, created = Metrics.objects.get_or_create(
            tg_id=instance.tg_id,
            defaults={'name': instance.name, 'registration_date': instance.subscription_signup_date or timezone.now()}
        )
        if not created:
            metrics.name = instance.name
            metrics.update_metrics()
            metrics.save()

@receiver(post_save, sender=Receipts)
def update_receipts_metrics(sender, instance, **kwargs):
    try:
        metrics = Metrics.objects.get(tg_id=instance.tg_id)
        metrics.spent += 100
        metrics.update_metrics()
    except Metrics.DoesNotExist:
        pass
    
@receiver(post_migrate)
def create_default_labels(sender, **kwargs):
    if not Labels.objects.exists():
        default_labels = {
            'give_number': 'Приветсвие\nНажмите "Поделиться номером" внизу экрана...',
            'error': 'Произошла ошибка. Попробуйте снова.',
            'name': 'Введите ваше имя',
            'surname': 'Введите ваша фамилия',
            'email': 'Введите ваш электронной почты',
            'thanks': 'Получить ссылку для оплаты',
            'get_link': 'Спасибо за регистрацию!',
            'menu': 'Выберите пункт меню',
            'platform': 'Чаты',
            'back': 'Вернуться назад.',
            'declined': 'Отказано',
            'next': 'Дальше',
            'all_done': 'Все готово!',
            'choose_tier': 'Выберите уровень подписки',
            'tier_1': 'Месяц',
            'tier_2': '2 месяца',
            'free_help': 'Получите бесплатную помощь',
            'club_discount': 'Скидка для членов клуба',
            'neuro_mark': 'Нейро-марк',
            'nearest_events': 'Ближайшие события',
            'library': 'Библиотека'
        }
        for label, text in default_labels.items():
            Labels.objects.create(name=label, text=text)
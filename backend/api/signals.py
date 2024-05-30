from django.db.models.signals import post_save
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
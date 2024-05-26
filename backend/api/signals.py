from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Labels
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
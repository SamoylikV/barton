from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import User, Labels, Chats, Events
from django.shortcuts import render, get_object_or_404
import sys
import os

@csrf_exempt
def create_user(request):
    tg_id = request.POST.get('tg_id')
    email = request.POST.get('email', '')
    number = request.POST.get('number')
    user, created = User.objects.get_or_create(tg_id=tg_id, defaults={'email': email, 'number': number})
    if not created:
        return JsonResponse({'message': 'User already exists'}, status=200)
    return JsonResponse({'message': 'User created'}, status=201)

@csrf_exempt
def update_user(request, tg_id):
    user = get_object_or_404(User, tg_id=tg_id)
    user.email = request.POST.get('email', user.email)
    user.number = request.POST.get('number', user.number)
    user.name = request.POST.get('name', user.name)
    user.surname = request.POST.get('surname', user.surname)
    user.subscription_signup_date = request.POST.get('subscription_signup_date', user.subscription_signup_date)
    user.subscription_expiration = request.POST.get('subscription_expiration', user.subscription_expiration)
    user.save()
    return JsonResponse({'message': 'User updated'}, status=200)

@csrf_exempt
def delete_user(request, tg_id):
    user = get_object_or_404(User, tg_id=tg_id)
    user.delete()
    return JsonResponse({'message': 'User deleted'}, status=200)

@csrf_exempt
def user_list(request):
    users = User.objects.all()
    data = [{"tg_id": user.tg_id, "email": user.email, "number": user.number} for user in users]
    return JsonResponse(data, safe=False)
@csrf_exempt
def user_detail(request, tg_id):
    user = get_object_or_404(User, tg_id=tg_id)
    data = {"tg_id": user.tg_id, "email": user.email, "number": user.number, "name": user.name, "surname": user.surname, "subscription_signup_date": user.subscription_signup_date, "subscription_expiration": user.subscription_expiration}
    return JsonResponse(data)

@csrf_exempt
def get_label_text(request, name):
    label = get_object_or_404(Labels, name=name)
    data = {"text": label.text}
    return JsonResponse(data)

@csrf_exempt
def get_all_labels(request):
    labels = Labels.objects.all()
    data = [{"name": label.name, "text": label.text, "tag": label.tag} for label in labels]
    return JsonResponse(data, safe=False)

@csrf_exempt
def get_chats(request):
    chats = Chats.objects.all()
    data = [{"chat_id": chat.chat_id, "chat_name": chat.chat_name} for chat in chats]
    return JsonResponse(data, safe=False)

@csrf_exempt
def get_events(request):
    events = Events.objects.all()
    data = [{"event_id": event.event_id, "event_name": event.event_name, "event_date": event.event_date} for event in events]
    return JsonResponse(data, safe=False)

@csrf_exempt
def get_message_by_id(request, message_id):
    if request.method == 'GET':
        message = Chats.objects.get(message_id=message_id)
        return JsonResponse({'message': message.message_text, 'date': message.date}, status=200)


@csrf_exempt
def trigger_send_message(request):
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
    from tg_bot.handlers import send_message_to_groups_sync
    if request.method == 'POST':
        message_id = request.POST.get('message_id')
        if message_id:
            try:
                send_message_to_groups_sync(int(message_id))
                return JsonResponse({'status': 'success'}, status=200)
            except Exception as e:
                return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
        else:
            return JsonResponse({'status': 'error', 'message': 'No message_id provided'}, status=400)
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)
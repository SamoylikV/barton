from django.shortcuts import render, get_object_or_404, redirect
from api.models import User, Labels, Events, Chats, Messages, Metrics
from .forms import LabelsForm, EventsForm, ChatsForm, MessageForm

def dashboard(request):
    users = User.objects.all()
    labels = Labels.objects.all()
    chats = Chats.objects.all()
    events = Events.objects.all()
    messages = Messages.objects.all()
    metrics = Metrics.objects.all()
    return render(request, 'admin_panel/dashboard.html', {'users': users, 'labels': labels, 'chats': chats, 'events': events, 'messages': messages, 'metrics': metrics})

def label_list(request):
    labels = Labels.objects.all()
    return render(request, 'admin_panel/label_list.html', {'labels': labels})

def label_detail(request, name):
    label = get_object_or_404(Labels, name=name)
    return render(request, 'admin_panel/label_detail.html', {'label': label})

def create_label(request):
    if request.method == "POST":
        form = LabelsForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('label_list')
    else:
        form = LabelsForm()
    return render(request, 'admin_panel/create_label.html', {'form': form, 'label': None})

def update_label(request, name):
    label = get_object_or_404(Labels, name=name)
    if request.method == "POST":
        form = LabelsForm(request.POST, instance=label)
        if form.is_valid():
            form.save()
            return redirect('label_list')
    else:
        form = LabelsForm(instance=label)
    return render(request, 'admin_panel/create_label.html', {'form': form, 'label': label})

def delete_label(request, name):
    label = get_object_or_404(Labels, name=name)
    if request.method == "POST":
        label.delete()
        return redirect('label_list')
    return render(request, 'admin_panel/delete_label.html', {'label': label})

def chat_list(request):
    chats = Chats.objects.all()
    return render(request, 'admin_panel/chat_list.html', {'chats': chats})

def create_chat(request):
    if request.method == "POST":
        form = ChatsForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('chat_list')
    else:
        form = ChatsForm()
    return render(request, 'admin_panel/chat_form.html', {'form': form, 'chat': None})

def update_chat(request, pk):
    chat = get_object_or_404(Chats, pk=pk)
    if request.method == "POST":
        form = ChatsForm(request.POST, instance=chat)
        if form.is_valid():
            form.save()
            return redirect('chat_list')
    else:
        form = ChatsForm(instance=chat)
    return render(request, 'admin_panel/chat_form.html', {'form': form, 'chat': chat})

def delete_chat(request, pk):
    chat = get_object_or_404(Chats, pk=pk)
    if request.method == "POST":
        chat.delete()
        return redirect('chat_list')
    return render(request, 'admin_panel/delete_chat.html', {'chat': chat})

def event_list(request):
    events = Events.objects.all()
    return render(request, 'admin_panel/event_list.html', {'events': events})

def create_event(request):
    if request.method == "POST":
        form = EventsForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('event_list')
    else:
        form = EventsForm()
    return render(request, 'admin_panel/event_form.html', {'form': form, 'event': None})

def update_event(request, pk):
    event = get_object_or_404(Events, pk=pk)
    if request.method == "POST":
        form = EventsForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            return redirect('event_list')
    else:
        form = EventsForm(instance=event)
    return render(request, 'admin_panel/event_form.html', {'form': form, 'event': event})

def delete_event(request, pk):
    event = get_object_or_404(Events, pk=pk)
    if request.method == "POST":
        event.delete()
        return redirect('event_list')
    return render(request, 'admin_panel/delete_event.html', {'event': event})

def message_list(request):
    messages = Messages.objects.all()
    return render(request, 'admin_panel/message_list.html', {'messages': messages})

def create_message(request):
    if request.method == 'POST':
        form = MessageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('message_list')
    else:
        form = MessageForm()
    return render(request, 'admin_panel/message_form.html', {'form': form, 'message': None})

def update_message(request, pk):
    message = get_object_or_404(Messages, pk=pk)
    if request.method == 'POST':
        form = MessageForm(request.POST, request.FILES, instance=message)
        if form.is_valid():
            form.save()
            return redirect('message_list')
    else:
        form = MessageForm(instance=message)
    return render(request, 'admin_panel/message_form.html', {'form': form, 'message': message})

def delete_message(request, pk):
    message = get_object_or_404(Messages, pk=pk)
    if request.method == 'POST':
        message.delete()
        return redirect('message_list')
    return render(request, 'admin_panel/message_confirm_delete.html', {'message': message})

def message_form(request, pk=None):
    if pk:
        message = get_object_or_404(Messages, pk=pk)
    else:
        message = Messages()

    if request.method == 'POST':
        form = MessageForm(request.POST, request.FILES, instance=message)
        if form.is_valid():
            form.save()
            return redirect('message_list')
    else:
        form = MessageForm(instance=message)
    
    return render(request, 'admin_panel/message_form.html', {'form': form})

def message_delete(request, pk):
    message = get_object_or_404(Messages, pk=pk)
    if request.method == 'POST':
        message.delete()
        return redirect('message_list')
    return render(request, 'admin_panel/message_confirm_delete.html', {'message': message})

def metrics_list(request):
    metrics = Metrics.objects.all()
    return render(request, 'admin_panel/metrics.html', {'metrics': metrics})
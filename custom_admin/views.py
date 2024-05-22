from django.shortcuts import render, get_object_or_404, redirect
from barton.models import User, Labels
from .forms import LabelsForm

def dashboard(request):
    users = User.objects.all()
    labels = Labels.objects.all()
    return render(request, 'admin_panel/dashboard.html', {'users': users, 'labels': labels})

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
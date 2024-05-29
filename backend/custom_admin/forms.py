from django import forms
from api.models import Labels, Events, Chats, Messages

class LabelsForm(forms.ModelForm):
    class Meta:
        model = Labels
        fields = ['name', 'text', 'tag']
        
class EventsForm(forms.ModelForm):
    class Meta:
        model = Events
        fields = ['name', 'text', 'date']
        
class ChatsForm(forms.ModelForm):
    class Meta:
        model = Chats
        fields = ['name', 'link']
        
class MessageForm(forms.ModelForm):
    class Meta:
        model = Messages
        fields = ['text', 'date', 'repeated', 'day_of_week', 'image']
        widgets = {
            'date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }
from django import forms
from barton.models import Labels, Events, Chats

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
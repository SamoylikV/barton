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
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.send_now:
            self.fields['date'].disabled = True
            self.fields['day_of_week'].disabled = True
            
    class Meta:
        model = Messages
        fields = ['text', 'date', 'repeated', 'day_of_week', 'image', 'send_now']
        widgets = {
            'date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }
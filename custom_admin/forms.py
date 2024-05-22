from django import forms
from barton.models import Labels

class LabelsForm(forms.ModelForm):
    class Meta:
        model = Labels
        fields = ['name', 'text', 'tag']
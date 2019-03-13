from django import forms
from .models import Text

class Record(forms.ModelForm):

    class Meta:
        model = Text
        fields = ['text']

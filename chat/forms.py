from django import forms
from .models import Message

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        # exclude sender/receiver/timestamp so only the text field remains
        exclude = ['sender', 'receiver', 'timestamp']
        widgets = {
            # adjust “text” here if your field is named differently
            'text': forms.Textarea(attrs={
                'rows': 2,
                'class': 'form-control',
                'placeholder': 'Type your message…'
            }),
        }

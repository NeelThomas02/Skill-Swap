from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django import forms
from .models import Profile
from skills.models import Skill

User = get_user_model()

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        # you can explicitly list fields or inherit the defaults
        fields = UserCreationForm.Meta.fields  

class ProfileForm(forms.ModelForm):
    skills = forms.ModelMultipleChoiceField(
        queryset=Skill.objects.all(),
        required=False,
        help_text="Check the skills you can offer.",
        # Each checkbox input will get the form-check-input class:
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'})
    )

    class Meta:
        model = Profile
        fields = ['bio', 'skills']
        widgets = {
            'bio': forms.Textarea(attrs={
                'rows': 3,
                'class': 'form-control',
                'placeholder': 'Tell people a bit about yourself…'
            }),
        }
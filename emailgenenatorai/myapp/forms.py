from django import forms
from .models import SubjectLine

class SubjectLineForm(forms.ModelForm):
    class Meta:
        model = SubjectLine
        fields = ['content']  # User input for generating the subject line

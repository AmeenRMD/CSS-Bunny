from django import forms
from .models import Level

class LevelForm(forms.ModelForm):
    class Meta:
        model = Level
        fields = [
            'level_number', 'title', 'instruction', 'css_property', 
            'correct_solution', 'bunny_count', 'carrot_count', 'difficulty'
        ]
        widgets = {
            'instruction': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
            'correct_solution': forms.Textarea(attrs={'rows': 3, 'class': 'form-control', 'placeholder': 'e.g. justify-content: flex-end;'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'css_property': forms.TextInput(attrs={'class': 'form-control'}),
            'level_number': forms.NumberInput(attrs={'class': 'form-control'}),
            'bunny_count': forms.NumberInput(attrs={'class': 'form-control'}),
            'carrot_count': forms.NumberInput(attrs={'class': 'form-control'}),
            'difficulty': forms.Select(attrs={'class': 'form-control'}),
        }

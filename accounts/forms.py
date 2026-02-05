from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.validators import RegexValidator

class SignUpForm(UserCreationForm):
    username = forms.CharField(
        max_length=150,
        help_text='Required. Letters, digits and underscore only.',
        validators=[
            RegexValidator(
                regex=r'^[\w]+$',
                message='Enter a valid username. This value may contain only letters, numbers, and underscore characters.',
                code='invalid_username'
            )
        ]
    )
    email = forms.EmailField(required=True, help_text='Required. A valid email address.')

    class Meta:
        model = User
        fields = ("username", "email")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user

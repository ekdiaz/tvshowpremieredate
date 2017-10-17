'''forms.py - Contains the forms used on the site.'''
from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms import EmailField

class SearchForm(forms.Form):
    '''Creates a search form for searching for a tv show.'''
    search_term = forms.CharField(label='Search term', max_length=100)

class UserCreationForm(UserCreationForm):
    '''Creates users with a username, email, and password.'''
    email = EmailField(label="Email", required=True, help_text="Required.")

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user

from django import forms

class AuthForm(forms.Form):
    username = forms.CharField(label='Username', max_length=64, min_length=1)
    password = forms.CharField(label='Password', widget=forms.PasswordInput(), 
                                max_length=1024, min_length=8)
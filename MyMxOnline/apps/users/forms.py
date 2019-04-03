from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(required=True)
    possword = forms.CharField(required=True)
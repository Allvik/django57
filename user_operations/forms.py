from django import forms


class account_form(forms.Form):
    nick = forms.CharField(max_length=20)
    password = forms.CharField(max_length=20)

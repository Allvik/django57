from django import forms


class AccountForm(forms.Form):
    nick = forms.CharField(max_length=20)
    password = forms.CharField(max_length=20)

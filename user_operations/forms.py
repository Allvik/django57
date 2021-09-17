from django import forms


class AccountForm(forms.Form):
    nick = forms.CharField(max_length=20, widget=forms.TextInput(attrs={'placeholder': 'Name'}))
    password = forms.CharField(max_length=20, widget=forms.TextInput(attrs={'placeholder': 'Password'}))

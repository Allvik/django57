from django import forms


class game_form(forms.Form):
    name = forms.CharField(max_length=30)
    short_name = forms.CharField(max_length=10)
    password = forms.CharField(max_length=20)

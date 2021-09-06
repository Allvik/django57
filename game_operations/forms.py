from django import forms


class create_game_form(forms.Form):
    name = forms.CharField(max_length=30)
    short_name = forms.CharField(max_length=10)
    password = forms.CharField(max_length=20)


class enter_game_form(forms.Form):
    short_name = forms.CharField(max_length=10)
    password = forms.CharField(max_length=20)

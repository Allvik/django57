from django import forms


class create_game_form(forms.Form):
    name = forms.CharField(max_length=30)
    short_name = forms.CharField(max_length=10)
    password = forms.CharField(max_length=20)
    count_rounds = forms.IntegerField(max_value=100, min_value=0)


class enter_game_form(forms.Form):
    short_name = forms.CharField(max_length=10)
    password = forms.CharField(max_length=20)

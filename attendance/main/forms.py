from django import forms

class imageFeedForm(forms.Form):
    image = forms.CharField()

class imageAttForm(forms.Form):
    batch = forms.CharField()
    section = forms.CharField()
    image = forms.CharField()
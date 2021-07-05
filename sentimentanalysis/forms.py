from django import forms


class dataForm(forms.Form):
    texte = forms.CharField(max_length=10000)
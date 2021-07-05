from django import forms


class chatbotForm(forms.Form):
    message = forms.CharField(max_length=10000)
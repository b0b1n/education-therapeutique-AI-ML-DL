from django import forms


class messageForm(forms.Form):
    message = forms.CharField(max_length=10000)

class PostForm(forms.Form):
    title = forms.CharField(max_length=100)
    body = forms.CharField(max_length=10000)
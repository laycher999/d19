from django import forms
from .models import Ad,Response, News
from tinymce.widgets import TinyMCE

class AdForm(forms.ModelForm):
    text = forms.CharField(widget=TinyMCE(attrs={'cols': 80, 'rows': 30}))
    class Meta:
        model = Ad
        fields = ['title', 'text', 'category', 'status']


class ResponseForm(forms.ModelForm):
    class Meta:
        model = Response
        fields = ['text']


class NewsForm(forms.ModelForm):
    text = forms.CharField(widget=TinyMCE(attrs={'cols': 80, 'rows': 30}))

    class Meta:
        model = News
        fields = ['title', 'text']
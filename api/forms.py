from django import forms

class SearchForm(forms.Form):
    title = forms.CharField(required=False)
    #year = forms.CharField(required=False)
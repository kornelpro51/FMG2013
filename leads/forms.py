from __future__ import unicode_literals
from django import forms
from jsonfield.forms import JSONFormField


class EmailForm(forms.Form):
    message = forms.CharField(widget=forms.Textarea)

class MandrillForm(forms.Form):
    mandrill_events = JSONFormField()
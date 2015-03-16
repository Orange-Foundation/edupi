from django import forms

from cntapp.models import Directory


class DirectoryForm(forms.Form):

    name = forms.CharField(label='New Folder', max_length=80)

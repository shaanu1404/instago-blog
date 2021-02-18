from django import forms

from .models import Tag

class AddTagForm(forms.Form):
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all().order_by('title'), 
        widget=forms.SelectMultiple(attrs={
                'class':'custom-control custom-select',
                'size': 10
            }),
            help_text='Hold down “Control”, or “Command” on a Mac, to select more than one.'
        )
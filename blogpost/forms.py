from django import forms
from django.utils.translation import gettext_lazy as _
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model

from .models import BlogPost

class CreateBlogPost(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ['title', 'body', 'content']

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'body': forms.Textarea(attrs={'class': 'form-control', 'rows': 2})
        }

        labels = {
            'title': _('Title'),
            'body': _('Description'),
            'content' : _('Content'),
        }

        """ More properties.
        help_texts = {
            'title': 'Enter the title of your blog.',
        }
        error_messages = {
            'title': {
                'max_length': "Your title is too long.",
            },
        }
        """

    # def clean_title(self):
    #     title = self.cleaned_data.get('title')
    #     if len(title) < 10:
    #         raise forms.ValidationError("Your title should be atleast 10 characters long.")

    #     return title

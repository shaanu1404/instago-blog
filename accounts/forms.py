from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django import forms

from .models import UserProfile

class RegistrationForm(forms.ModelForm):
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password']
        labels = {
            'email' : 'Email'
        }
        widgets = {
            "username" :  forms.TextInput(attrs={'class': 'form-control'}),
            "first_name" :  forms.TextInput(attrs={'class': 'form-control'}),
            "last_name" :  forms.TextInput(attrs={'class': 'form-control'}),
            "email" :  forms.EmailInput(attrs={'class': 'form-control'}),
            "password" :  forms.PasswordInput(attrs={'class': 'form-control'}),
        }

    def clean_confirm_password(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError('Password didn\'t match.')
        return confirm_password

    def clean_password(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError('Password didn\'t match.')
        return password

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('Username already exists.')
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Email already exists.')
        return email

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        # Save the provided password in hashed format
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class LoginAuthForm(AuthenticationForm):
    username = forms.CharField(widget = forms.TextInput(attrs={'class':'form-control'}))
    password = forms.CharField(widget = forms.PasswordInput(attrs={'class':'form-control'}))



class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name')

        widgets = {
            'first_name' : forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'last_name' : forms.TextInput(attrs={'class': 'form-control', 'required': True}),
        }

class UserProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('bio', 'profile_image')

        widgets = {
            'bio' : forms.Textarea(attrs={'class': 'form-control', 'rows': '2'}),
        }

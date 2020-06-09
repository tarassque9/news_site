from django import forms
from .models import User, Comment, Post, ModerationPost
from .other import RequiredFieldsMixin


class PostCreateForm(forms.ModelForm):    
    class Meta:
        model = Post
        fields = ['title', 'text']
    # def test_valid(self):
    #     data = self.cleaned_data['title']
    #     if 'aa' in data:
    #         raise forms.ValidationError('Invalid value')
    #     return data


class RegistrationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'password', 'first_name', 'last_name', 'date_of_birth']
        # fields_required = ['first_name', 'last_name', 'date_of_birth']
        widgets = {
            'email': forms.TextInput(attrs={'class': 'form-control'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'date_of_birth': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
        }


class LoginForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'password']
        widgets = {
            'email': forms.TextInput(attrs={'class': 'form-group'}),
            'password': forms.PasswordInput(attrs={'class': 'form-group'})
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']


class ModerationForm(forms.ModelForm):
    class Meta:
        model = ModerationPost
        fields = ['title', 'text']

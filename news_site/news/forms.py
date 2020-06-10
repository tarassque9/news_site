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
        fields = ['email', 'password', 'first_name',
                  'last_name', 'date_of_birth']
        # fields_required = ['first_name', 'last_name', 'date_of_birth']
        form_control = {'class': 'form-control'}
        widgets = {
            'email': forms.TextInput(attrs=form_control),
            'password': forms.PasswordInput(attrs=form_control),
            'first_name': forms.TextInput(attrs=form_control),
            'last_name': forms.TextInput(attrs=form_control),
            'date_of_birth': forms.DateInput(attrs={'type': 'date',
                                                    'class': 'form-control'})
        }


class LoginForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'password']
        #exclude = ['first_name', 'last_name', 'date_of_birth']
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

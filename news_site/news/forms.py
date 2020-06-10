from django import forms
from .models import User, Comment, Post, ModerationPost
from .other import RequiredFieldsMixin
from django.core.exceptions import ValidationError


class PostCreateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'text']

    # def test_valid(self):
    #     data = self.cleaned_data['title']
    #     if 'aa' in data:
    #         raise forms.ValidationError('Invalid value')
    #     return data


# class RegistrationForm(forms.ModelForm):
#     class Meta:
#         model = User
#         fields = ['email', 'password', 'first_name',
#                   'last_name', 'date_of_birth']
#         # fields_required = ['first_name', 'last_name', 'date_of_birth']
#         form_control = {'class': 'form-control'}
#         widgets = {
#             'email': forms.TextInput(attrs=form_control),
#             'password': forms.PasswordInput(attrs=form_control),
#             'first_name': forms.TextInput(attrs=form_control),
#             'last_name': forms.TextInput(attrs=form_control),
#             'date_of_birth': forms.DateInput(attrs={'type': 'date',
#                                                     'class': 'form-control'})
#         }

class RegistrationForm(forms.Form):
    form_control = {'class': 'form-control'}
    email = forms.EmailField(max_length=255, widget=forms.EmailInput(attrs=form_control))
    password = forms.CharField(max_length=100, widget=forms.PasswordInput(attrs=form_control))
    first_name = forms.CharField(max_length=100, required=False, widget=forms.TextInput(attrs=form_control))
    last_name = forms.CharField(max_length=100, required=False, widget=forms.TextInput(attrs=form_control))
    date_of_birth = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}))

    def clean_pass(self):
        data = self.cleaned_data['password']
        print(data)
        if len(data) < 5:
            raise forms.ValidationError("You have forgotten about Fred!")
            print('[error]')
        return data

    
# class LoginForm(forms.ModelForm):
#     class Meta:
#         model = User
#         fields = ['email', 'password']
#         #exclude = ['first_name', 'last_name', 'date_of_birth']
#         widgets = {
#             'email': forms.TextInput(attrs={'class': 'form-group'}),
#             'password': forms.PasswordInput(attrs={'class': 'form-group'})
#         }

class LoginForm(forms.Form):
    form_control = {'class': 'form-control'}
    email = forms.EmailField(max_length=255, widget=forms.EmailInput(attrs=form_control))
    password = forms.CharField(max_length=100, widget=forms.PasswordInput(attrs=form_control))
    #print('[AFTER FORMS]')

    def clean_pass(self):
        data = self.cleaned_data['password']
        print(data)
        if len(data) < 5:
            raise forms.ValidationError("You have forgotten about Fred!")
            print('[error]')
        return data



class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']


class ModerationForm(forms.ModelForm):
    class Meta:
        model = ModerationPost
        fields = ['title', 'text']

from django.contrib import admin
from django import forms
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from .models import User, Post, Comment, ModerationPost


from django.contrib import admin
from django.http import HttpResponseRedirect
from django.conf.urls import url

from django.urls import reverse

from django.template.response import TemplateResponse
from django.urls import path
#from monitor.models import LoginMonitor
#from monitor.import_custom import ImportCustom

# @admin.register(ModerationPost)
# class LoginMonitorAdmin(admin.ModelAdmin):
#     change_list_template = "admin/change_form.html"
#     def get_urls(self):
#         urls = super().get_urls()
#         custom_urls = [
#             url('^import/$', self.process_import, name='process_import'),
#             ]
#         return custom_urls + urls
#     def process_import_btmp(self, request):
#         pass
#         import_custom = ImportCustom()
#         count = import_custom.import_data()
#         self.message_user(request, f"создано {count} новых записей")
#         return HttpResponseRedirect("../")

from django.contrib import admin
from django.urls import reverse

admin.site.register([User, Post, Comment])

@admin.register(ModerationPost)
class AdminModeration(admin.ModelAdmin):

    change_form_template = "admin/change_form.html"

    fieldsets = (
        (None, {
            'fields': ('title', 'text')
        }),
        # ('Advanced options', {
        #     'classes': ('collapse',),
        #     'fields': (),
        # }),
    )

    def get_urls(self):
        urls = super().get_urls()
        #print(urls)
        my_urls = [
            path('my_view', self.my_view, name='home')
        ]
        return my_urls + urls

    def my_view(self, request):
        val = 12345
        context = dict(
           # Include common variables for rendering the admin template.
           self.admin_site.each_context(request),
           # Anything else you want in the context...
           val,
           
        )
        return TemplateResponse(request, "submit_line.html", context)
    
    

    









# class AdminModerationPostForm(forms.ModelForm):

#     class Meta:
#         model = ModerationPost
#         fields = ['title', 'text']

# class UserCreationForm(forms.ModelForm):
#     """A form for creating new users. Includes all the required
#     fields, plus a repeated password."""
#     password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
#     password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

#     class Meta:
#         model = User
#         fields = ['email']

#     def clean_password2(self):
#         # Check that the two password entries match
#         password1 = self.cleaned_data.get("password1")
#         password2 = self.cleaned_data.get("password2")
#         if password1 and password2 and password1 != password2:
#             raise forms.ValidationError("Passwords don't match")
#         return password2

#     def save(self, commit=True):
#         # Save the provided password in hashed format
#         user = super().save(commit=False)
#         user.set_password(self.cleaned_data["password1"])
#         if commit:
#             user.save()
#         return user


# class UserChangeForm(forms.ModelForm):
#     """A form for updating users. Includes all the fields on
#     the user, but replaces the password field with admin's
#     password hash display field.
#     """
#     password = ReadOnlyPasswordHashField()

#     class Meta:
#         model = User
#         fields = ('email', 'password', 'is_active', 'is_admin')

#     def clean_password(self):
#         # Regardless of what the user provides, return the initial value.
#         # This is done here, rather than on the field, because the
#         # field does not have access to the initial value
#         return self.initial["password"]


# class UserAdmin(BaseUserAdmin):
#     # The forms to add and change user instances
#     form = UserChangeForm
#     add_form = UserCreationForm

#     # The fields to be used in displaying the User model.
#     # These override the definitions on the base UserAdmin
#     # that reference specific fields on auth.User.
#     list_display = ('email', 'is_admin')
#     list_filter = ('is_admin',)
#     fieldsets = (
#         (None, {'fields': ('email', 'password')}),
#         ('Personal info', {'fields': ('date_of_birth',)}),
#         ('Permissions', {'fields': ('is_admin',)}),
#     )
#     # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
#     # overrides get_fieldsets to use this attribute when creating a user.
#     add_fieldsets = (
#         (None, {
#             'classes': ('wide',),
#             'fields': ('email', 'date_of_birth', 'password1', 'password2'),
#         }),
#     )
#     search_fields = ('email',)
#     ordering = ('email',)
#     filter_horizontal = ()


# Now register the new UserAdmin...
#admin.site.register(User, UserAdmin)
#admin.site.register([User, Post, Comment, AdminModerationPostForm])
#admin.site.register(ModerationPost, AdminModerationPostForm)
# ... and, since we're not using Django's built-in permissions,
# unregister the Group model from admin.
#admin.site.unregister(Group)

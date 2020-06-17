from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Post, Comment, ModerationPost
from django.conf.urls import url
from django.template.response import TemplateResponse
from django.urls import path


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
        my_urls = [
            path('my_view', self.my_view, name='home')
        ]
        return my_urls + urls

    def my_view(self, request):
        context = dict(
           # Include common variables for rendering the admin template.
           self.admin_site.each_context(request),
           # Anything else you want in the context...
        )
        return TemplateResponse(request, "submit_line.html", context)

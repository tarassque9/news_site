# all operation with save, delete to database
from .models import User, Comment, Post, ModerationPost
from django.shortcuts import render,get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse

def create_comment(text, user, post):
    comment = Comment(text=text, user=user, post=post)
    comment.save()
    #comment_notification.delay(post.user.email)

#def save_moderation_post()

class UserCreateMixin:
    form = None

    def get(self, request):
        bound_form = self.form(request.POST)
        return render(request, self.template_name, context={'form': bound_form})

    def post(self, request):
        bound_form = self.form(request.POST)
        emails_queryset = User.objects.values('email')
        if bound_form.is_valid():
            email = bound_form.cleaned_data['email']
            if emails_queryset.filter(email=email).exists():
                print('[error]')
            password = bound_form.cleaned_data['password']
            first_name = bound_form.cleaned_data['first_name'] or None
            last_name = bound_form.cleaned_data['last_name'] or None
            date_of_birth = bound_form.cleaned_data['date_of_birth'] or None
            new_user = User(email=email, password=password,
                            first_name=first_name, last_name=last_name,
                            date_of_birth=date_of_birth)
            new_user.set_password(new_user.password)
            new_user.save()
            link = f'http://127.0.0.1:8000/news/verification/{new_user.uuid}/'
            # send_mail.delay(email, link)
            login(request, new_user)
            return HttpResponseRedirect('/news')
        return HttpResponse('[REGISTRATION FORM IS NOT VALID]')
            

            


from django.shortcuts import render
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from .models import User, Post, Comment, ModerationPost
from .forms import PostCreateForm, RegistrationForm,\
                            LoginForm, CommentForm, ModerationForm
from django.contrib.auth.views import LogoutView
from .permissions import AdminPermissionsMixin, IsVerificationUserMixin
from .tasks import send_mail, comment_notification
from .other import clear_text, uuid_gen
from .custom import CustomBackend
from logs import logger
from .services import UserCreateMixin


class HomeView(View):
    template_name = 'news/home.html'

    def get(self, request):
        posts = Post.objects.order_by('-created')
        form = CommentForm()
        comments = Comment.objects.all
        context = {'posts': posts,
                   'form': form,
                   'comments': comments}
        return render(request, self.template_name, context=context)

    def post(self, request, id):
        """ Create comment """
        form = CommentForm(request.POST)
        if form.is_valid():
            text = form.cleaned_data['text']
            user = request.user
            post = Post.objects.get(id=id)
            comment = Comment(text=text, user=user, post=post)
            comment.save()
            comment_notification.delay(post.user.email)
            return HttpResponseRedirect('/news')
        msg = f'Comment was not created'
        logger.warning(msg + f'by user {user.username}')
        return HttpResponse(msg)


class PostCreateView(View):
    template_name = 'news/post_create.html'

    def get(self, request):
        form = PostCreateForm()
        return render(request, self.template_name, context={'form': form})

    def post(self, request):
        role = request.user.role
        if role == 3:
            form = ModerationForm(request.POST)
            if form.is_valid():
                text = clear_text(form.cleaned_data['text'])
                title = clear_text(form.cleaned_data['title'])
                user = request.user.id
                moderation = ModerationPost(title=title,
                                            text=text,
                                            moderation_status=user)
                moderation.save()
                logger.info(f'{request.user.username} created the post that was sent to moderation')
                return HttpResponseRedirect('/news')
            logger.warning(f'form by user {request.user.username} [NOT VALID]')
            return HttpResponse('[POST CREATE FORM NOT VALID]')
        elif role == 1 or 2:
            form = PostCreateForm(request.POST)
            if form.is_valid():
                text = clear_text(form.cleaned_data['text'])
                title = clear_text(form.cleaned_data['title'])
                user = User.objects.get(id=request.user.id)
                post = Post(title=title, text=text, user=user)
                post.save()
                return HttpResponseRedirect('/news')
            return HttpResponse('[POST CREATE FORM NOT VALID]')
        return HttpResponse('[ERROR]')


# class PostDetail(View):
#     template_name = 'news/post_detail.html'

#     def get(self, request, id):
#         post = Post.objects.get(id=id)
#         return render(request, self.template_name, context={'post': post})




class RegistrationView(View):
    template_name = 'news/registration.html'

    def get(self, request):
        form = RegistrationForm(request.POST)
        return render(request, self.template_name, context={'form': form})

    def post(self, request):
        form = RegistrationForm(request.POST)
        if bound_form.is_valid():
            save_user()

    


class LoginView(View, CustomBackend):
    template_name = 'news/login.html'

    def get(self, request):
        form = LoginForm()
        return render(request, self.template_name, context={'form': form})

    def post(self, request):
        form = LoginForm(request.POST)
        # form is not_valid? why?
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(email=email, password=password)
        login(request, user)
        return HttpResponseRedirect('/news')


class LogoutView(LogoutView):
    pass


class ModerationView(AdminPermissionsMixin, View):
    template_name = 'news/moderation.html'

    def get(self, request):
        posts = ModerationPost.objects.order_by('-created')
        form = ModerationForm()
        context = {'posts': posts, 'form': form}
        return render(request, self.template_name, context=context)


class ModerationAccept(View):
    template_name = 'news/moderation.html'

    def get(self, request, id):
        moder_post = ModerationPost.objects.get(id=id)
        user_id = moder_post.moderation_status
        user = User.objects.get(id=user_id)
        post = Post(title=moder_post.title, text=moder_post.text, user=user)
        moder_post.delete()
        post.save()
        return HttpResponseRedirect('/news/moderation')


class ModerationDecline(View):
    template_name = 'news/moderation.html'

    def get(self, request, id):
        moder_post = ModerationPost.objects.get(id=id)
        moder_post.delete()
        return HttpResponseRedirect('/news/moderation')


class VerificationView(View):
    template_name = 'news/test.html'

    def get(self, request, uuid):
        users = User.objects.all()
        for user in users:
            if uuid in user.uuid:
                user.verification = True
                user.save()
                return HttpResponse('[VERIFICATION ACCEPT]')

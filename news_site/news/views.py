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
from .services import UserCreateMixin, create_comment
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.shortcuts import get_list_or_404, get_object_or_404


class HomeView(View):
    template_name = 'news/home.html'

    def get(self, request):
        search_query = request.GET.get('search', '')
        if search_query:
            post_list = Post.objects.filter(Q(title__icontains=search_query) |
                                            Q(text__icontains=search_query))
        else:
            post_list = Post.objects.order_by('-created')

        form = CommentForm()
        comments = get_list_or_404(Comment)
        page = request.GET.get('page', 1)
        paginator = Paginator(post_list, 2)
        try:
            posts = paginator.page(page)
        except PageNotAnInteger:
            posts = paginator.page(1)
        except EmptyPage:
            posts = paginator.page(paginator.num_pages)
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
            create_comment(text, user, post)
            logger.info(f'Comment was created by {user.email}')
            return HttpResponseRedirect('/news')
        msg = f'Comment was not created'
        logger.info(msg + f'by user {user.email}')
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
                logger.info(f'{request.user.email} created the post\
                            that was sent to moderation')
                return HttpResponseRedirect('/news')
            logger.info(f'form by user {request.user.email} [NOT VALID]')
            return HttpResponse('[POST CREATE FORM NOT VALID]')
        elif role == 1 or 2:
            form = PostCreateForm(request.POST)
            if form.is_valid():
                text = clear_text(form.cleaned_data['text'])
                title = clear_text(form.cleaned_data['title'])
                user = get_object_or_404(User, pk=request.user.id)
                post = Post(title=title, text=text, user=user)
                post.save()
                logger.info(f'{request.user.email} created the post')
                return HttpResponseRedirect('/news')
            logger.info(f'form by user {request.user.email} [NOT VALID]')
            return HttpResponse('[POST CREATE FORM NOT VALID]')
        logger.warning(f'[SOME ERROR WITH USER ROLE]')
        return HttpResponse('[ERROR]')


class PostDetail(View):
    template_name = 'news/post_detail.html'

    def get(self, request, id):
        post = Post.objects.get(id=id)
        return render(request, self.template_name, context={'post': post})


class RegistrationView(View):
    template_name = 'news/registration.html'

    def get(self, request):
        form = RegistrationForm(request.POST)
        return render(request, self.template_name, context={'form': form})

    def post(self, request):
        bound_form = RegistrationForm(request.POST)
        emails_queryset = User.objects.values('email')
        if bound_form.is_valid():
            email = bound_form.cleaned_data['email']
            if emails_queryset.filter(email=email).exists():
                return HttpResponse('[USER WITH CURRENT EMAIL ALREADY EXISTS]')
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
            send_mail.delay(email, link)
            login(request, new_user)
            return HttpResponseRedirect('/news')
        return HttpResponse('[REGISTRATION FORM IS NOT VALID]')


class LoginView(View, CustomBackend):
    template_name = 'news/login.html'

    def get(self, request):
        form = LoginForm()
        return render(request, self.template_name, context={'form': form})

    def post(self, request):
        form = LoginForm(request.POST)
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(email=email, password=password)
        login(request, user)
        logger.debug(f'User with email: {user.email} login')
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
        # user = User.objects.get(id=user_id)
        user = get_object_or_404(User, pk=user_id)
        post = Post(title=moder_post.title, text=moder_post.text, user=user)
        moder_post.delete()
        logger.info(f'Post with title: {post.title} delete from moderation\
                    and submitted for publication')
        post.save()
        logger.info(f'Post with title: {post.title} was published')
        return HttpResponseRedirect('/news/moderation')


class ModerationDecline(View):
    template_name = 'news/moderation.html'

    def get(self, request, id):
        # moder_post = ModerationPost.objects.get(id=id)
        moder_post = get_object_or_404(ModerationPost, pk=id)
        moder_post.delete()
        logger.info(f'Post with title: {moder_post.title} was decline')
        return HttpResponseRedirect('/news/moderation')


class VerificationView(View):
    template_name = 'news/test.html'

    def get(self, request, uuid):
        users = get_list_or_404(User)
        for user in users:
            if uuid in user.uuid:
                user.verification = True
                user.save()
                logger.info(f'User with email: {user.email} verificated')
                return HttpResponse('[VERIFICATION ACCEPT]')
            logger.info(f'User verification with email: {user.email} decline')
            return HttpResponse('[Verification Decline]')

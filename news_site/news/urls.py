from django.urls import path

from .views import HomeView, PostCreateView, RegistrationView, PostDetail, LoginView, LogoutView, ModerationView, ModerationAccept, ModerationDecline, VerificationView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('comment/<int:id>/', HomeView.as_view(), name='comment'),
    path('post_detail/<int:id>/', PostDetail.as_view(), name='post_detail'),
    path('post_create/', PostCreateView.as_view(), name='post_create'),
    path('registration/', RegistrationView.as_view(), name='registration'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('moderation/', ModerationView.as_view(), name='moderation'),
    path('moderation/<int:id>/accept/', ModerationAccept.as_view(), name='moderation_accept'),
    path('moderation/<int:id>/decline/', ModerationDecline.as_view(), name='moderation_decline'),
    path('verification/<uuid>/', VerificationView.as_view(), name='verification')   
]

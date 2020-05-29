from django.http import Http404
from .models import User
from django.contrib.auth.mixins import LoginRequiredMixin

class AdminPermissionsMixin(LoginRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user.role == 1:
            return super().dispatch(request, *args, **kwargs)
        return self.handle_no_permission()

class IsVerificationUserMixin(LoginRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        if request.user.verification:
            return super().dispatch(request, *args, **kwargs)
        return self.handle_no_permission()       
    
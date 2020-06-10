# all operation with save, delete to database
from .models import User
from django.shortcuts import render,get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse

# class ObjectCreateMixin:
#     form_model = None
#     template = None

#     def get(self, request):
#         form = self.form_model()
#         return render(request, self.template, context={'form': form})


#     def post(self,request):
#         bound_form = self.form_model(request.POST)

#         if bound_form.is_valid():
#             new_obj = bound_form.save()
#             return redirect(new_obj)
#         return render(request, self.template, context={'form': bound_form})

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
            

            


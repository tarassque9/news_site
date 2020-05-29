from django.shortcuts import redirect

def redirect_news(request):
    return redirect('home', permanent=True)

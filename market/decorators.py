from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect

def authenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('home')
        else:
            return view_func(request, *args, **kwargs)

    return wrapper_func
# coding=utf-8
from django.shortcuts import render, redirect, render_to_response, get_object_or_404
from django.template import loader
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
# from .forms import LoginForm
from django.template.context import RequestContext
from django.contrib import auth
from .forms import RegisterForm
from models import User


def index(request):
    context = {}
    template = loader.get_template('app/login.html')
    return HttpResponse(template.render(context, request))


def gentella_html(request):
    context = {}
    # The template to be loaded as per gentelella.
    # All resource paths for gentelella end in .html.

    # Pick out the html file name from the url. And load that template.
    load_template = request.path.split('/')[-1]
    template = loader.get_template('app/' + load_template)
    return HttpResponse(template.render(context, request))


# def login(request):
#     if request.method == 'GET':
#         form = LoginForm()
#         return render_to_response('app/login.html', RequestContext(request, {'form': form, }))
#     else:
#         form = LoginForm(request.POST)
#         if form.is_valid():
#             username = request.POST.get('username', '')
#             password = request.POST.get('password', '')
#             user = auth.authenticate(username=username, password=password)
#             if user is not None and user.is_active:
#                 auth.login(request, user)
#                 return render_to_response('app/index.html', RequestContext(request))
#             else:
#                 return render_to_response('app/login.html', RequestContext(request, {'form': form, 'password_is_wrong': True}))
#         else:
#             return render_to_response('app/login.html', RequestContext(request, {'form': form, }))

# def logout(request):
#     auth.logout(request)
#     return HttpResponseRedirect('app/login.html')

def register(request):
    redirect_to = request.POST.get('next', request.GET.get('next', ''))
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            if redirect_to:
                return redirect(redirect_to)
            else:
                return redirect('login.html')
    else:
        form = RegisterForm()
    return render(request, 'app/register.html', context={'form': form, 'next': redirect_to})

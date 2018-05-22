# coding=utf-8
from __future__ import print_function
from django.shortcuts import render, redirect, render_to_response, get_object_or_404
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
# from django.contrib.auth import authenticate, login, logout
# from django.contrib.auth.decorators import login_required
from django.template.context import RequestContext
from django.contrib import auth
from .forms import RegisterForm, LoginForm
from django.contrib.auth.models import Permission
from django.contrib.auth import models
from django.http import JsonResponse
from .utils import serialize_bootstraptable
from .models import User
from django.views.decorators.csrf import csrf_exempt
import json



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


@csrf_exempt
def do_login(request):
    if request.method == 'GET':
        form = LoginForm()
        return render_to_response('app/login.html', RequestContext(request, {'form': form, }))
    else:
        form = LoginForm(request.POST)
        if form.is_valid():
            username = request.POST.get('username', '')
            password = request.POST.get('password', '')
            user = auth.authenticate(username=username, password=password)
            if user is not None and user.is_active:
                auth.login(request, user)
                return render_to_response('app/index.html', RequestContext(request))
            else:
                return render_to_response('app/login.html', RequestContext(request, {'form': form, 'password_is_wrong': True}))
        else:
            return render_to_response('app/login.html', RequestContext(request, {'form': form, }))


def do_logout(request):
    auth.logout(request)
    return HttpResponseRedirect('login.html')


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


def show_group(request):
    group = auth.models.Group.objects.all()
    return render(request, 'app/show_group.html', context={'group': group})


def get_group(request):
    group = auth.models.Group.objects.all()
    group_send = serialize_bootstraptable(group)
    # return render(request, 'app/show_group.html', context={'group': group})
    return JsonResponse(group_send)


@csrf_exempt
def del_group(request):
    status = {'status': False}
    if request.method == "POST":
        received_json_data = json.loads(request.body)
        print(received_json_data)
        for i in received_json_data:
            groupid = (i['id'])
            deletesql = models.Group.objects.filter(id=groupid)  # 执行删除操作
            if deletesql.delete():
                status = {'status': True}
            else:
                status = {'status': False}
    return JsonResponse(status)


def show_stu(request):
    return render(request, 'app/show_stu.html')


def get_stu(request):
    stu = User.objects.filter(groups__id='2')
    stuid_send = serialize_bootstraptable(stu)
    return JsonResponse(stuid_send)

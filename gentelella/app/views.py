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


def get_group(request):
    # per = Permission.objects.get()
    group = auth.models.Group.objects.all()

    return render(request, 'app/show_group.html', context={'group': group})


def group_delete(request):
    if request.method == "POST":
        groupid = request.POST.get('groupid')
        print("id = %s" % groupid)
        status = "删除成功！"
        result = "Error!"
        deletesql = models.Group.objects.filter(id=groupid)  # 执行删除操作
        if deletesql.delete():
            return HttpResponse(json.dumps({
                "status": status
            }))
        else:
            return HttpResponse(json.dumps({
                "result": result
            }))


def del_group(request):
    ret = {'status': True}
    try:
        groupid = request.GET.get('groupid')
        models.Group.objects.filter(id=groupid).delete()
    except Exception as e:
        ret['status'] = False
    return HttpResponse(json.dumps(ret))

# def add_student(request):
#     response = {'status': True, 'message': None, 'data': None}
#     try:
#         u = request.POST.get('username')
#         a = request.POST.get('age')
#         g = request.POST.get('gender')
#         c = request.POST.get('cls_id')
#         obj = models.Student.objects.create(
#             username=u,
#             age=a,
#             gender=g,
#             cs_id=c
#         )
#         response['data'] = obj.id
#     except Exception as e:
#         response['status'] = False
#         response['message'] = '用户输入错误'
#
#     result = json.dumps(response, ensure_ascii=False)
#     return HttpResponse(result)
#
#
# def del_student(request):
#     ret = {'status': True}
#     try:
#         nid = request.GET.get('nid')
#         models.Student.objects.filter(id=nid).delete()
#     except Exception as e:
#         ret['status'] = False
#     return HttpResponse(json.dumps(ret))
#
#
# def edit_student(request):
#     response = {'code': 1000, 'message': None}
#     try:
#         nid = request.POST.get('nid')
#         user = request.POST.get('user')
#         age = request.POST.get('age')
#         gender = request.POST.get('gender')
#         cls_id = request.POST.get('cls_id')
#         models.Student.objects.filter(id=nid).update(
#             username=user,
#             age=age,
#             gender=gender,
#             cs_id=cls_id
#         )
#     except Exception as e:
#         response['code'] = 1001
#         response['message'] = str(e)
#     return HttpResponse(json.dumps(response))
#
#
# def test_ajax_list(request):
#     print(request.POST.getlist('k'))
#     return HttpResponse('...')
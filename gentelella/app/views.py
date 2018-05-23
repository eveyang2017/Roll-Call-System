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
from .models import User, Course
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import PageNotAnInteger, Paginator, InvalidPage, EmptyPage
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
    group_send = serialize_bootstraptable(group, group.count())
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
    if request.method == "GET":
        limit = request.GET.get('limit')
        offset = request.GET.get('offset')
        if not limit:
            limit = 10
        if not offset:
            offset = 0
        stu = User.objects.filter(groups__id='2')
        pageinator = Paginator(stu, limit)
        page = int(int(offset) / int(limit) + 1)
        stu_page_info = pageinator.page(page).object_list
        stu_count = stu.count()
        stu_send = serialize_bootstraptable(stu_page_info, stu_count)
    return JsonResponse(stu_send)


def show_course(request):
    return render(request, 'app/show_course.html')


@csrf_exempt
def get_course(request):
    course = Course.objects.all()
    course_send = serialize_bootstraptable(course, course.count())
    return JsonResponse(course_send)

# @csrf_exempt
# def get_course(request):
#     data = request.POST  # 获取 bootstrap-table post请求的数据，直接POST获取！
#     queryResult = Course.objects.all()  # 去数据库查询
#     if queryResult == 0:
#         return HttpResponse('0')
#
#     elif queryResult == -1:
#         return HttpResponse('-1')
#
#     else:
#         '''服务端分页时，前端需要传回：limit（每页需要显示的数据量），offset（分页时 数据的偏移量，即第几页）'''
#         '''mysql 利用 limit语法 进行分页查询'''
#         '''服务端分页时，需要返回：total（数据总量），rows（每行数据）  如： {"total": total, "rows": []}'''
#         returnData = {"rows": []}  #########非常重要############
#         with open("slg/others/country", "r") as f:
#             datas = json.loads(f.read())  # 直接读出来，是dic对象，用key，value获取。。。上面的是转换为 对象了，可以用 “.” 获取
#         '''遍历 查询结果集'''
#         for results in queryResult:
#             '''遍历 country.json 输出 订单状态'''
#             for data in datas['order']:
#                 if data['stateNum'] == str(results['purchasestate']):
#                     orderStateResult = data['stateResult']
#
#             '''遍历 country.json 输出 国家名称'''
#             for data in datas['country']:
#                 if data['shorthand'] == results['countrycode']:
#                     countryName = data['name']
#
#             returnData['rows'].append({
#                 "id": results['gameorderid'],
#                 "name": results['orderid'],
#                 "category": results['nickname'],
#                 "credit": "Wrath",
#                 "hours": results['purchasetimes'],
#                 "teacher": str(results['priceamount']),
#                 "desc": orderStateResult,
#             })
#         # 最后用dumps包装下，json.dumps({"rows": [{"gameorderid": 1}, {"gameorderid": 22}]})
#         return HttpResponse(json.dumps(returnData))
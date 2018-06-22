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
from .models import User, Course, Department, CS, Place
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from django.core.paginator import PageNotAnInteger, Paginator, InvalidPage, EmptyPage
from django.core.serializers import serialize
import json


def index(request):
    context = {}
    template = loader.get_template('app/login.html')
    return HttpResponse(template.render(context, request))


def go_index(request):
    return render(request, 'app/index.html')


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
    flag = 1
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
                stu = User.objects.filter(groups__id='2')
                for i in stu:
                    if user == i:
                        print(i.username)
                        flag = 0
                if flag == 1: 
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
    return render(request, 'app/show_group.html')


def get_group(request):
    group = auth.models.Group.objects.all()
    group_send = serialize_bootstraptable(group, group.count())
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


@csrf_exempt
def add_stu(request):
    status = {'status': False}
    print(request.body)
    if request.method == "POST":
        num = request.POST.get('num')
        first_name = request.POST.get('first_name')
        college = request.POST.get('college')
        faculty = request.POST.get('faculty')
        new_user = User.objects.create(
            num=num,
            first_name=first_name,
            college=college,
            faculty=faculty,
            username=num,
            password='pbkdf2_sha256$30000$HPvJqS3PjSo1$ynYiqwekwkZTYlvXPBuA7NOtEEadBx32ZInz/wUD8q4='
        )
        u = User.objects.get(username=num)
        u.set_password('123456')
        u.save()
        if new_user:
            if new_user.groups.add(2):
                status = {'status': True}
    return JsonResponse(status)


@csrf_exempt
def del_stu(request):
    status = {'status': False}
    if request.method == "POST":
        received_json_data = json.loads(request.body)
        print(received_json_data)
        for i in received_json_data:
            stu_num = (i['num'])
            deletesql = User.objects.filter(num=stu_num)  # 执行删除操作
            if deletesql.delete():
                status = {'status': True}
            else:
                status = {'status': False}
    return JsonResponse(status)


@csrf_exempt
def update_stu(request):
    status = {'status': False}
    print(request.body)
    if request.method == "POST":
        id = request.POST.get('id')
        num = request.POST.get('num')
        first_name = request.POST.get('first_name')
        college = request.POST.get('college')
        faculty = request.POST.get('faculty')
        new_stu_info = User.objects.select_for_update().filter(id=id).update(
            num=num,
            first_name=first_name,
            college=college,
            faculty=faculty,
        )
        if new_stu_info:
            status = {'status': True}
    return JsonResponse(status)


@csrf_exempt
def show_course(request):
    return render(request, 'app/show_course.html')


@csrf_exempt
def get_course(request):
    if request.method == "GET":
        limit = request.GET.get('limit')
        offset = request.GET.get('offset')
        if not limit:
            limit = 10
        if not offset:
            offset = 0
        course = Course.objects.all()
        pageinator = Paginator(course, limit)
        page = int(int(offset) / int(limit) + 1)
        course_page_info = pageinator.page(page).object_list
        course_send = serialize_bootstraptable(course_page_info, course.count())
    return JsonResponse(course_send)


@csrf_exempt
def add_course(request):
    status = {'status': False}
    print(request.body)
    if request.method == "POST":
        name = request.POST.get('name')
        category = request.POST.get('category')
        credit = request.POST.get('credit')
        hours = request.POST.get('hours')
        desc =request.POST.get('desc')
        new_course = Course.objects.create(
            name=name,
            category=category,
            credit=credit,
            hours=hours,
            desc=desc,
        )
        if new_course:
            status = {'status': True}
    return JsonResponse(status)


@csrf_exempt
def update_course(request):
    status = {'status': False}
    print(request.body)
    if request.method == "POST":
        id = request.POST.get('id')
        name = request.POST.get('name')
        category = request.POST.get('category')
        credit = request.POST.get('credit')
        hours = request.POST.get('hours')
        desc = request.POST.get('desc')
        new_course_info = Course.objects.select_for_update().filter(id=id).update(
            name=name,
            category=category,
            credit=credit,
            hours=hours,
            desc=desc)
        if new_course_info:
            status = {'status': True}
    return JsonResponse(status)


@csrf_exempt
def del_course(request):
    status = {'status': False}
    if request.method == "POST":
        received_json_data = json.loads(request.body)
        print(received_json_data)
        for i in received_json_data:
            courseid = (i['id'])
            print(courseid)
            deletesql = Course.objects.filter(id=courseid)  # 执行删除操作
            print(deletesql)
            if deletesql.delete():
                status = {'status': True}
            else:
                status = {'status': False}
    return JsonResponse(status)


def show_dep(request):
    return render(request, 'app/show_dep.html')


def get_dep(request):
    dep = Department.objects.all()
    json_data = serialize('json', dep)
    data = json.loads(json_data)
    dep_send = []
    for i in data:
        f_item = i["fields"]
        f_parentid = f_item["parentID"]
        if f_parentid:
            continue
        else:
            f_id = f_item["iid"]
            f_name = f_item["name"]
            dep_data = {"id": f_id, "text": f_name, "children": []}
            for p in data:
                c_item = p["fields"]
                c_parentid = c_item["parentID"]
                if c_parentid == f_id:
                    c_id = c_item["iid"]
                    c_name = c_item["name"]
                    c_data = {"id": c_id, "text": c_name, "children": []}
                    for j in data:
                        c2_item = j["fields"]
                        c2_parentid = c2_item["parentID"]
                        if c2_parentid == c_id:
                            c2_id = c2_item["iid"]
                            c2_name = c2_item["name"]
                            c2_data = {"id": c2_id, "text": c2_name, "children": []}
                            for k in data:
                                c3_item = k["fields"]
                                c3_parentid = c3_item["parentID"]
                                if c3_parentid == c2_id:
                                    c3_id = c3_item["iid"]
                                    c3_name = c3_item["name"]
                                    c3_data = {"id": c3_id, "text": c3_name}
                                    c2_data["children"].append(c3_data)
                            c_data["children"].append(c2_data)
                    dep_data["children"].append(c_data)
            dep_send.append(dep_data)

    return HttpResponse(json.dumps(dep_send))


def show_cs(request):
    return render(request, 'app/show_cs.html')


@csrf_exempt
def get_cs(request):
    if request.method == "GET":
        limit = request.GET.get('limit')
        offset = request.GET.get('offset')
        if not limit:
            limit = 10
        if not offset:
            offset = 0
        cs = CS.objects.all()
        pageinator = Paginator(cs, limit)
        page = int(int(offset) / int(limit) + 1)
        cs_page_info = pageinator.page(page).object_list
        cs_send = serialize_bootstraptable(cs_page_info, cs.count())
    return JsonResponse(cs_send)


def show_place(request):
    return render(request, 'app/show_place.html')

@csrf_exempt
def get_place(request):
    if request.method == "GET":
        limit = request.GET.get('limit')
        offset = request.GET.get('offset')
        if not limit:
            limit = 10
        if not offset:
            offset = 0
        place = Place.objects.all()
        pageinator = Paginator(place, limit)
        page = int(int(offset) / int(limit) + 1)
        place_page_info = pageinator.page(page).object_list
        place_send = serialize_bootstraptable(place_page_info, place.count())
    return JsonResponse(place_send)


@csrf_exempt
def add_place(request):
    status = {'status': False}
    print(request.body)
    if request.method == "POST":
        name = request.POST.get('name')
        dep = request.POST.get('dep')        
        comment =request.POST.get('comment')
        new_place = Place.objects.create(
            name=name,
            dep=dep,
            comment=comment,
        )
        if new_place:
            status = {'status': True}
    return JsonResponse(status)


@csrf_exempt
def update_place(request):
    status = {'status': False}
    print(request.body)
    if request.method == "POST":
        id = request.POST.get('id')
        name = request.POST.get('name')
        dep = request.POST.get('dep')        
        comment =request.POST.get('comment')
        new_place_info = Place.objects.select_for_update().filter(id=id).update(
            name=name,
            dep=dep,
            comment=comment,
        )
        if new_place_info:
            status = {'status': True}
    return JsonResponse(status)


@csrf_exempt
def del_place(request):
    status = {'status': False}
    if request.method == "POST":
        received_json_data = json.loads(request.body)
        print(received_json_data)
        for i in received_json_data:
            courseid = (i['id'])
            print(courseid)
            deletesql = Place.objects.filter(id=courseid)  # 执行删除操作
            print(deletesql)
            if deletesql.delete():
                status = {'status': True}
            else:
                status = {'status': False}
    return JsonResponse(status)


@csrf_exempt
def api_login(request):
    status = {'status': False}
    if request.method == "POST":
        received_json_data = json.loads(request.body)
        print(received_json_data)
        username = received_json_data['username']
        password = received_json_data['password']
        user = auth.authenticate(username=username, password=password)
        if user is not None and user.is_active:
            userinfo = User.objects.filter(username=username)
            print(userinfo)
            status = serialize_bootstraptable(userinfo, userinfo.count())
        else:
            status = {'status': False}
    return JsonResponse(status)


from django.conf.urls import url, include
from app import views

urlpatterns = [
    # Matches any html file - to be used for gentella
    # Avoid using your .html in your resources.
    # Or create a separate django app.
    url(r'^.*\.html', views.gentella_html, name='gentella'),

    # The home page
    url(r'^$', views.index, name='index'),
    # login
    url(r'app/login/$', views.do_login, name='do_login'),
    url(r'app/register/', views.register, name='register'),
    url(r'app/logout/', views.do_logout, name='do_logout'),
    url(r'app/', include('django.contrib.auth.urls')),
    url(r'app/show_group/', views.show_group, name='show_group'),
    url(r'app/get_group/$', views.get_group),
    url(r'app/del_group/$', views.del_group),
    url(r'app/show_stu/', views.show_stu, name='show_stu'),
    url(r'app/get_stu/$', views.get_stu),
    url(r'app/show_course/', views.show_course, name='show_course'),
    url(r'app/get_course/$', views.get_course),
    url(r'app/add_course/$', views.add_course),
    url(r'app/update_course/$', views.update_course),
    url(r'app/del_course/$', views.del_course),
]

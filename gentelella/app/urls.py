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
    url(r'app/login/', views.do_login, name='do_login'),
    url(r'app/register/', views.register, name='register'),
    # url(r'app/logout/', views.do_logout, name='do_logout'),
    url(r'^app/', include('django.contrib.auth.urls')),
]

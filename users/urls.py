"""OOD_Project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import url
import users.views

urlpatterns = [
    url(r'^login/$', users.views.loginView, name='login'),
    url(r'^logout/$', users.views.logoutAj, name='logout'),
    url(r'^base/$', users.views.baseView, name='base-view'),
    url(r'^register/$', users.views.showRegisterKUser, name='register'),
    url(r'^dismiss/$', users.views.showDismissKUser, name='dismiss'),
    url(r'^change-pass/$', users.views.showChangePass, name='change-pass'),
    url(r'^report-user-activity/$', users.views.showReportUserActivity, name='show-report-user-activity'),
    url(r'^special-privilege-request/$', users.views.showSpecialprivilageRequest, name='show-special-privilege-request'),
    url(r'^request-manager/$', users.views.showRequestManager, name='show-request-manager'),
    url(r'^user-profile/(?P<user_id>\d+)$', users.views.userProfileView, name='show-user-profile'),

    url(r'^search/user/$', users.views.searchUser, name='show-search-user'),
]

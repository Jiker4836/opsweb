#coding:utf8
from django.conf.urls import include, url
from . import views
from dashboard import user
from dashboard.user import group

urlpatterns = [
    url(r'^login/$', views.LoginView.as_view()),
    url(r'^logout/$', views.LogoutView.as_view()),
    url(r'^$', views.IndexView.as_view()),
    url(r'permission/', include([
        url(r'none/$', views.permission),
    ])),

    url(r'^user/', include([
    	url(r'^userlist/$',user.UserListView.as_view()),
    	url(r'^modifystatus/$',user.ModifyUserStatusView.as_view()),
    	url(r'^modifydepartment/$', user.ModifyDepartmentView.as_view()),
    	url(r'^modifyphone/$',user.ModifyUserPhoneView.as_view()),
    	])),

    url(r'^group/', include([
            url(r'^l$',group.GroupView.as_view()),
            url(r'^list/$',group.GroupListView.as_view()),
            url(r'^usergroup/$',group.UserGroupView.as_view()),
            url(r'^permission/$',group.GroupPermissionListView.as_view()),
            url(r'^permissions/$',group.GroupPermissionView.as_view()),
            url(r'^userpermission/$',group.UserGroupPermissionListView.as_view()),
    	])),
 ]
#coding:utf8
from django.conf.urls import include, url
from . import views
from dashboard import user
from dashboard.user import group
from dashboard.server import idc,server,product
from dashboard.monitor import zabbix


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
            url(r'^$',group.GroupView.as_view()),
            url(r'^list/$',group.GroupListView.as_view()),
            url(r'^usergroup/$',group.UserGroupView.as_view()),
            url(r'^permission/$',group.GroupPermissionListView.as_view()),
            url(r'^permissions/$',group.GroupPermissionView.as_view()),
            url(r'^userpermission/$',group.UserGroupPermissionListView.as_view()),
    	])),

    url(r'^server/',include([
            url(r'^idc/',include([
                    url(r'add/$',idc.AddIdcView.as_view(),name='idc_add'),
                    url(r'list/$',idc.IdcListView.as_view(),name='idc_list'),
                ])),

                url(r'^product/', include([
                        url(r'^manage',include([
                            url(r'^/$',product.ProductMangeView.as_view(),name="product_manage"),
                            url(r'/add/$',product.ProductAddView.as_view(),name="product_add"),
                            url(r'/get/$',product.ProductMangeGetView.as_view(),name="product_manage_get"),
                            ])),
                    ])),

            url(r'report/$',server.ServerInfoAutoReport.as_view()),
            url(r'^list/$',server.ServerListView.as_view(),name="server_list"),
            url(r'^status/$',server.ModifyServerStatusView.as_view(),name="modify_server_status"),
        ])),

    url(r'^monitor/',include([
                url(r'^zabbix/', include([
                    # url(r'hostrsync/$',server.MonitorZabbixHostrsync.as_view(),name='monitory_zabbix_hostrsync'),
                    url(r'hostrsync/$',zabbix.HostRsyncView.as_view(),name='monitory_zabbix_hostrsync'),
                    ])),
        ])),
   
 ]

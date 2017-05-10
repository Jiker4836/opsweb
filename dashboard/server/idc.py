#coding:utf8
from django.shortcuts import render
from django.http import HttpResponse,JsonResponse,QueryDict
from django.template import Context,loader,RequestContext
from django.contrib.auth import authenticate, login, logout
from django.views.generic import View,TemplateView, ListView, RedirectView, FormView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required, permission_required
from dashboard.forms import IdcForm
from dashboard.models import Idc
from django.core.urlresolvers import reverse
from django.conf import settings

import logging
logger=logging.getLogger('opsweb')

class AddIdcView(TemplateView):
	template_name="server/add_idc.html"

	@method_decorator(login_required)
	@method_decorator(permission_required("dashboard.add_idc",login_url=settings.PERMISSION_NONE_URL))
	def get(self,request,*args,**kwargs):
		return super(AddIdcView,self).get(request,*args,**kwargs)	

	@method_decorator(login_required)
 	@method_decorator(permission_required("dashboard.add_idc",login_url=settings.PERMISSION_NONE_URL))
	def post(self,request):
		ret={'status':0,"next_url":reverse("idc_list")}
		form=IdcForm(request.POST)
		if form.is_valid():
			try:
				idc=Idc(**form.cleaned_data)
				idc.save()
			except Exception as e:
				errmsg="用户{} 添加IDC出错: {}".format(request.user.username,e.args)
				logger.error(errmsg)
				ret["status"]=1
				ret["errmsg"]=errmsg
		else:
			errmsg="用户{} 添加IDC验证失败: {}".format(request.user.username, form.errors.as_json())
			logger.error(errmsg)
			ret["status"]=1
			ret["errmsg"]=errmsg			
		return render(request,settings.TEMPLATE_JUMP,ret)

class IdcListView(ListView):
	template_name="server/idc_list.html"
	model=Idc

	@method_decorator(login_required)
	@method_decorator(permission_required("dashboard.view_idc",login_url=settings.PERMISSION_NONE_URL))
	def get(self,request,*args,**kwargs):
		return super(IdcListView,self).get(request,*args,**kwargs)	

class SysReportView(View):

	def post(self,request):
		ret={'status':0,"next_url":reverse("idc_list")}
		return JsonResponse(ret,safe=True)
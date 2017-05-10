#coding:utf8
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse,JsonResponse,QueryDict
from django.template import Context,loader,RequestContext
from django.contrib.auth import authenticate, login, logout
from django.views.generic import View,TemplateView, ListView, RedirectView, FormView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required, permission_required
from dashboard.forms import IdcForm
from dashboard.models import Idc,Server,Status
from django.core.urlresolvers import reverse
from django.conf import settings
import datetime

import logging
logger=logging.getLogger('opsweb')


class ServerInfoAutoReport(View):
	'''接收client网上汇报的数据'''
	def post(self,rquest):
		data=self.request.POST.dict()
		try:
			Server.objects.get(uuid=data.get('uuid',""))
			data['check_update_time']=datetime.datetime.now()
			Server.objects.filter(uuid=data['uuid']).update(**data)
		except Server.DoesNotExist:
			s=Server(**data)
			s.save()
		except Exception as e:
			logger.error("sysinfo 同步失败{}".format(e.args))
		return HttpResponse("")

class ServerListView(ListView):
	model=Server
	template_name="server/server_list.html"
	paginate_by=10
	before_index=6
	after_index=5

	def get_queryset(self):
		queryset=super(ServerListView,self).get_queryset()
		hostname=self.request.GET.get('hostname','').strip().lower()
		inner_ip=self.request.GET.get('inner_ip','').strip().lower()
		queryset=queryset.filter(hostname__contains=hostname)
		queryset=queryset.filter(inner_ip__contains=inner_ip)
		return queryset

	def get_context_data(self,**kwargs):
		context=super(ServerListView,self).get_context_data(**kwargs)
		page_obj=context["page_obj"]
		context["page_range"]=self.get_page_range(page_obj)
		context.update(self.request.GET.dict())
		context['uri']=self.get_uri()
		return context

	def get_uri(self):
		args=self.request.GET.copy()
		pop_key=['amp','page']
		for k in pop_key:
			if args.has_key(k):
				args.pop(k)
		return args.urlencode()

	def get_page_range(self,page_obj):
		start_index=page_obj.number-self.before_index
		if start_index<0:
			start_index=0
		return page_obj.paginator.page_range[start_index:page_obj.number+self.after_index]

	def get(self,request,*args,**kwargs):
		return super(ServerListView,self).get(request,*args,**kwargs)

class ModifyServerStatusView(TemplateView):
	template_name = "server/modify_server_status.html"

	def get_context_data(self, **kwargs):
	    context = super(ModifyServerStatusView, self).get_context_data(**kwargs)
	    context['status_obj'] = get_object_or_404(Server, pk=self.request.GET.get('server_id', None))
	    context['statuslist'] = Status.objects.all()
	    return context

	def get(self,request,*args,**kwargs):
		return super(ModifyServerStatusView,self).get(request,*args,**kwargs)	

	def post(self,request):
		server_id = request.POST.get('server_id', None)
		status=request.POST.get("status","")
		ret={"status":0,"next_url":reverse("server_list")}
		next_url=request.GET.get('next',"")
		if next_url:
			ret["next_url"]=next_url
		obj=get_object_or_404(Server,pk=server_id)
		try:
			obj.status=status
			obj.save()
		except Exception as e:
			ret["status"]=1
			ret["errmsg"]=e.args
		print ret
		return 	render(request,settings.TEMPLATE_JUMP,ret)	
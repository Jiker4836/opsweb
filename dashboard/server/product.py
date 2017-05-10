#coding:utf8
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse,JsonResponse,QueryDict
from django.template import Context,loader,RequestContext
from django.contrib.auth import authenticate, login, logout
from django.views.generic import View,TemplateView, ListView, RedirectView, FormView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User
from dashboard.forms import IdcForm
from dashboard.forms.product import ProductForm
from dashboard.models import Idc,Server,Status,Product
from django.core.urlresolvers import reverse
from django.conf import settings
import datetime


import logging
logger=logging.getLogger('opsweb')

class ProductMangeView(ListView):
	template_name="server/product_manage.html"
	model=Product
	paginate_by=10
	before_index=6
	after_index=5

	def get_queryset(self):
		queryset=super(ProductMangeView,self).get_queryset()
		name=self.request.GET.get('name','').strip().lower()
		module_letter=self.request.GET.get('module_letter','').strip().lower()
		queryset=queryset.filter(name__contains=name)
		queryset=queryset.filter(module_letter__contains=module_letter)
		return queryset

	def get_context_data(self,**kwargs):
		context=super(ProductMangeView,self).get_context_data(**kwargs)
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
		return super(ProductMangeView,self).get(request,*args,**kwargs)

class ProductAddView(TemplateView):
	template_name="server/product_add.html"

	def get_context_data(self,**kwargs):
		context=super(ProductAddView,self).get_context_data(**kwargs)
		context["user_object_list"]=User.objects.all()
		return context	

	def post(self,request):
		ret={"status":0,"next_url":reverse("idc_list")}
		print request.POST
		form=ProductForm(request.POST)
		if form.is_valid():
			try:
				product=Product(**form.cleaned_data)
				product.save()
			except Exception as e:
				msg="用户{}业务线出错:{}".format(request.user.username,e.args)
				logger.error(msg)
				ret['status']=1
				ret['errmsg']=msg
		else:
			msg="用户{} 添加业务线验证失败:{}".format(request.user.username,form.errors.as_json())
			logger.error(msg)
			ret['status']=1
			ret['errmsg']=msg			
		return HttpResponse("")
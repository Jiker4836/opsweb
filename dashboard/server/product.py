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
import datetime,json


import logging
logger=logging.getLogger('opsweb')


class Ztree(object):

	def __init__(self):
		self.data=self._get_products()

	def _get_products(self):
		return Product.objects.all()

	def _get_second_product(self,pid):
		return [ obj for obj in self.data if obj.p_product is not None and obj.p_product.id==pid ]

	def get(self,async=False):
		ret=[]
		#根据p_product为None获取一级业务线
		one_product=[p_obj for p_obj in self.data if p_obj.p_product is None]
		for one_obj in one_product:
			two_product=self._get_second_product(one_obj.id)
			tmp={}
			tmp['pid']=0
			tmp['id']=one_obj.id
			tmp['name']=one_obj.name
			tmp['children']=[]
			for child in two_product:
				children_node={'pid':one_obj.id,'name':child.name,'id':child.id}
				if async:
					children_node['isParent']=True
				tmp['children'].append(children_node)
			ret.append(tmp)
		return ret

class ProductMangeView(TemplateView):
	template_name="server/product_manage.html"

	def get_context_data(self,**kwargs):
		context=super(ProductMangeView,self).get_context_data(**kwargs)
		context['znodes']=json.dumps(Ztree().get())
		return context

class ProductMangeGetView(View):
	def get(self,request):
		ret={'status':0,'errmsg':''}
		id=request.GET.get('id',0)
		try:
			product_obj=Product.objects.get(pk=id)
			product_data=product_obj.__dict__
		except Product.DoesNotExist:
			ret['status']=1
			ret['errmsg']=u"该记录不存在"
		else:
			product_data=product_obj.__dict__
			if  product_data['p_product_id'] is None:
				product_data['p_product_id']="顶级"
			else:
				product_data['p_product_id']=product_obj.p_product.name
			del product_data['_state']
			if product_data.has_key("_p_product_cache"):
				del product_data["_p_product_cache"]
			ret['data']=product_data
		return JsonResponse(ret,safe=True)


class ProductAddView(TemplateView):
	template_name="server/product_add.html"

	def get_context_data(self,**kwargs):
		context=super(ProductAddView,self).get_context_data(**kwargs)
		context["user_object_list"]=User.objects.all()
		context['p_products']=Product.objects.filter(p_product__isnull=True)
		return context	

	def post(self,request):
		ret={"status":0,"next_url":reverse("idc_list")}
		print request.POST
		form=ProductForm(request.POST)
		if form.is_valid():
			try:
				product=Product(**form.cleaned_data)
				print form.cleaned_data
				product.save()
			except Exception as e:
				msg=u"用户{}业务线出错:{}".format(request.user.username,e.args)
				logger.error(msg)
				ret['status']=1
				ret['errmsg']=msg
		else:
			msg=u"用户{} 添加业务线验证失败:{}".format(request.user.username,form.errors.as_json())
			logger.error(msg)
			ret['status']=1
			ret['errmsg']=msg
		ret['next_url']=reverse("product_manage")			
		return render(request,settings.TEMPLATE_JUMP,ret)
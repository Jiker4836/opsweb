#coding:utf8
from django.shortcuts import render
from django.http import HttpResponse,JsonResponse,QueryDict
from django.template import Context,loader,RequestContext
from django.contrib.auth import authenticate, login, logout
from django.views.generic import View,TemplateView, ListView, RedirectView, FormView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required, permission_required
import datetime,time

import logging
logger=logging.getLogger('opsweb')

class IndexView(View):
	@method_decorator(login_required)
	def get(self,request):
		return render(request,"public/index.html")

class LoginView(View):
	def get(self,request):
		return render(request,"user/login.html",{"title":"reboot 运维平台"})

	def post(self,request):
		ret={"status":0}
		username=request.POST.get("username")
		password=request.POST.get("password")
		user=authenticate(username=username,password=password)
		if user is not None:
			if user.is_active:
				login(request,user)
				# request.session.set_expiry(30)#设置30秒后过期
				#设置session登陆后第二天2点过期，django会同时设置cookie过期
				nowtime=time.time()
				tomorrow=datetime.date.today()+datetime.timedelta(days=1)
				tomorrowtime='%s 02:00:00' %(tomorrow)
				timestamp=time.mktime(time.strptime(tomorrowtime,'%Y-%m-%d %H:%M:%S'))
				request.session.set_expiry(timestamp-nowtime)
				ret["next_url"]=request.GET.get('next') if  request.GET.get('next',None) else '/'
			else:
				ret["status"]=1
				ret["errmsg"]="用户被禁止"
		else:
			ret["status"]=2
			ret["errmsg"]="用户或密码错误"			
		return JsonResponse(ret,safe=True)		

class LogoutView(View):
	@method_decorator(login_required)
	def get(self,request,*args,**kwargs):
		logout(self.request)
		return HttpResponse("用户退出成功")

@login_required
def permission(request):
	return render(request, 'public/permission.html')
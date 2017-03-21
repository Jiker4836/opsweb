#coding:utf8
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required, permission_required
from django.views.generic import View,TemplateView, ListView, RedirectView, FormView
from django.contrib.auth.models import User
from django.http import HttpResponse,JsonResponse,Http404,QueryDict
from django.core.paginator import Paginator,EmptyPage
from django.contrib.auth.models import User,Group,Permission,ContentType
from dashboard.models import Department, Profile
from django.conf import settings
from django.shortcuts import render
import logging
from django.core import serializers

class GroupListView(ListView):
	model=Group
	template_name="user/grouplist.html"

	@method_decorator(login_required)
 	@method_decorator(permission_required("auth.view_group_list",login_url=settings.PERMISSION_NONE_URL))
	def get(self,request,*args,**kwargs):
		return super(GroupListView,self).get(request,*args,**kwargs)	

	def post(self,request):
		ret={"status":0}
		if not request.user.has_perm("auth.add_group"):
			ret["status"]=1
			ret["errmsg"]="没有权限"
			return JsonResponse(ret,safe=True)
			
		name=request.POST.get('name',"")
		if name:
			try:
				group=Group()
				group.name=name
				group.save()
			except Exception as e:
				ret["status"]=1
				ret["errmsg"]=e.args
		return JsonResponse(ret,safe=True)

class GroupView(View):
	@method_decorator(login_required)
    	def get(self, request):
        		uid = request.GET.get('uid', '')
        		ret = {'status': 0}
        		try:
        			user = User.objects.get(pk=uid)
        		except User.DoesNotExist as e:
        			ret['status'] = 1
        			ret['errmsg'] = '用户不存在{}'.format(e.args)
        		all_groups = Group.objects.all()
        		groups = [group for group in all_groups if group not in user.groups.all()]
        		return HttpResponse(serializers.serialize("json", groups), content_type="application/json")
		
class UserGroupView(View):
	'''
	取出指定用户组下的所有用户信息
	'''
	@method_decorator(login_required)
	def get(self,request):
		gid=request.GET.get('gid',None)
		try:
			group=Group.objects.get(pk=gid)
		except Exception as e:
			return JsonResponse([],safe=False)
		users=group.user_set.all()
		user_list=[{"username":user.username,"email":user.email,"name":user.profile.name} for user in users]
		return JsonResponse(user_list,safe=False)
	'''
	将用户添加到指定组
	'''
	@method_decorator(login_required)
    	@method_decorator(permission_required("auth.add_group", login_url=settings.PERMISSION_NONE_URL))
	def post(self,request):
		ret={"status":0}
		uid=request.POST.get('uid',None)
		gid=request.POST.get('gid',None)
		try:
			user=User.objects.get(pk=uid)
		except User.DoesNotExist:		
			logger.error("将用户添加至指定用户组，用户不存在，用户id为：{}".format(uid))
			ret["status"]=1
			ret["errmsg"]="用户不存在"
			return JsonResponse(ret,safe=True)
		except group.DoesNotExist:
			logger.error("将用户组添加至指定用户组，用户组不存在，用户id为：{}".format(uid))
			ret["status"]=1
			ret["errmsg"]="用户组不存在"
			return JsonResponse(ret,safe=True)	
		user.groups.add(group)
		return JsonResponse(ret,safe=True)

	@method_decorator(login_required)
    	@method_decorator(permission_required("auth.add_group", login_url=settings.PERMISSION_NONE_URL))
	def delete(self,request):
		ret={"status":0}
		data=QueryDict(request.body)
		uid=data.get('userid',None)
		gid=data.get('groupid',None)
		try:
			user=User.objects.get(pk=uid)
			group=Group.objects.get(pk=gid)
		except User.DoesNotExist:
			logger.error("将用户添加至指定用户组，用户不存在，用户id为：{}".format(uid))
			ret["status"]=1
			ret["errmsg"]="用户不存在"
		except group.DoesNotExist:
			logger.error("将用户组添加至指定用户组，用户组不存在，用户id为：{}".format(uid))
			ret["status"]=1
			ret["errmsg"]="用户组不存在"
		except Exception as e:
			ret["status"]=1
			ret["errmsg"]=e.args
		return JsonResponse(ret,safe=True)

class GroupPermissionListView(TemplateView):
	template_name="user/group_permission_list.html"

	def get_context_data(self,**kwargs):
		context=super(GroupPermissionListView,self).get_context_data(**kwargs)
		context['group']=self.request.GET.get('gid',None)
		context['group_permissions']=self.get_group_permission()
		context["content_type"]=ContentType.objects.all()
		return context	

	def get_group_permission(self):
		gid=self.request.GET.get('gid',None)
		try:
			group=Group.objects.get(pk=gid)
			return [per.id for per in group.permissions.all()]
		except Group.DoesNotExist as e:
			logger.error("用户组{}不存在".format(e.args))
			raise Http404

 	@method_decorator(login_required)
 	@method_decorator(permission_required("auth.view_group_list",login_url=settings.PERMISSION_NONE_URL))
	def get(self,request,*args,**kwargs):
		return super(GroupPermissionListView,self).get(request,*args,**kwargs)

	@method_decorator(login_required)
    	@method_decorator(permission_required("auth.add_group", login_url=settings.PERMISSION_NONE_URL))
	def post(self,request):
		permission_id_list=request.POST.getlist('permission',[])
		groupid=request.POST.get('group',None)
		ret = {"status": 0, "next_url": "/group/list/"}
		try:
			group=Group.objects.get(pk=groupid)
		except  Group.DoesNotExist as e:
			logger.error("用户组不存在{}".format(e.args))
			ret["status"]=1
			ret["errmsg"]="用户组不存在"
		else:
			if permission_id_list:
				permission_objs=Permission.objects.filter(id__in=permission_id_list)
				group.permissions=permission_objs
		return  render(request, settings.TEMPLATE_JUMP, ret)


class UserGroupPermissionListView(View):
	def get(self,request):
		gid=self.request.GET.get('gid',None)
		glist=[]
		try:
			for i in gid.split(','):
				group=Group.objects.get(pk=i)
				for per in group.permissions.all():
					glist.append((per.id,per.name,per.codename))
			return JsonResponse(glist,safe=False)
		except Group.DoesNotExist:
			raise Http404

class GroupPermissionView(TemplateView):
	template_name="user/group_permissions.html"

	def get_context_data(self, **kwargs):
		context_data = super(GroupPermissionView, self).get_context_data(**kwargs)
	  	gid=self.request.GET.get('gid',0)
	    	try:
	    		group=Group.objects.get(pk=gid)
	    		context_data['permissions']=group.permissions.all()
	    	except Group.DoesNotExist as e:
	    		raise Http404
	    	return context_data

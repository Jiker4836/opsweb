#coding:utf8
from django.views.generic import TemplateView,View,ListView
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.http import HttpResponse,JsonResponse,Http404
from django.core.paginator import Paginator,EmptyPage
from django.contrib.auth.models import User
from dashboard.models import Department, Profile
from django.conf import settings
import logging
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required, permission_required

logger=logging.getLogger('opsweb')

class UserListView(ListView):
	template_name="user/userlist.html"
	model=User
	paginate_by=5
	before_index=6
	after_index=5

	def get_queryset(self):
		queryset=super(UserListView,self).get_queryset()
		username=self.request.GET.get('username',None)
		if username:
			queryset=queryset.filter(username__contains=username)
		return queryset

	def get_context_data(self,**kwargs):
		context=super(UserListView,self).get_context_data(**kwargs)
		page_obj=context["page_obj"]
		context["page_range"]=self.get_page_range(page_obj)
		return context

	def get_page_range(self,page_obj):
		start_index=page_obj.number-self.before_index
		if start_index<0:
			start_index=0
		return page_obj.paginator.page_range[start_index:page_obj.number+self.after_index]




class ModifyUserStatusView(View):
	def post(self,request):
		ret={"status":0}
		user_id=request.POST.get("user_id",None)
		try:
			user=User.objects.get(pk=user_id)
			if user.is_active:
				user.is_active=False
			else:
				user.is_active=True
			user.save()
		except User.DoesNotExist:
			ret["status"]=1
			ret["errmsg"]="用户不存在"
		return JsonResponse(ret,safe=True)

class ModifyDepartmentView(TemplateView):
    template_name = "user/modify_department.html"

    def get_context_data(self, **kwargs):
        context = super(ModifyDepartmentView, self).get_context_data(**kwargs)
        context['user_obj'] = get_object_or_404(User, pk=self.request.GET.get('user', None))
        context['departments'] = Department.objects.all()
        return context

    def post(self, request):
        user_id = request.POST.get('id', None)
        department_id = request.POST.get('department', None)
        if not user_id or not department_id:
            raise Http404

        try:
            user_obj = User.objects.get(pk=user_id)
            # 通过id 查询用户
            department_obj = Department.objects.get(pk=department_id)
            # 通过id查询部门
        except:
            # 查询不到结果则报错
            raise Http404
        else:
            # 修改部门的的id,后保存
            user_obj.profile.department = department_obj
            user_obj.profile.save()
        return redirect("/user/userlist/")

    def get(self, request, *args, **kwargs):
        self.request = request
        return super(ModifyDepartmentView, self).get(request, *args, **kwargs)		

class ModifyUserPhoneView(TemplateView):
	template_name="user/modify_phone.html"

	def get_context_data(self,**kwargs):
		context=super(ModifyUserPhoneView,self).get_context_data(**kwargs)
		uid=self.request.GET.get('uid')
		context['user_obj']=self.get_user_obj(uid)
		return context

	def post(self,request):
		uid=request.POST.get('id',None)
		user_obj=self.get_user_obj(uid)
		user_obj.profile.phone=request.POST.get('phone',None)
		user_obj.profile.save()
		# return HttpResponse('')
		print settings.TEMPLATE_JUMP
		return render(request,settings.TEMPLATE_JUMP,{"status":0,"next_url":"/user/userlist/"})

	def get_user_obj(self,uid):
		try:
			return User.objects.get(pk=uid)
		except User.DoesNotExist:
			raise Http404
		except User.MultipleObjectsReturned:
			#返回多条记录
			pass


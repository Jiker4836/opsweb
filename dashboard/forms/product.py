#coding:utf8
from django import forms
from django.contrib.auth.models import User

class ProductForm(forms.Form):
	name=forms.CharField(required=True,max_length=32,error_messages={"required":"业务线名称不能为空","max_length":"长度必须小于32"})
	module_letter=forms.CharField(required=True,max_length=10,error_messages={"required":"业务线字母简称不能为空","max_length":"长度必须小于10"})
	p_product=forms.CharField(required=True)
	op_interface=forms.MultipleChoiceField(choices=((user_obj.username,user_obj.email) for user_obj in User.objects.all()) )
	dev_interface=forms.MultipleChoiceField(choices=((user_obj.username,user_obj.email) for user_obj in User.objects.all()) )

	def clean_module_letter(self):
		module_letter=self.cleaned_data.get('module_letter')
		return module_letter

	def clean_p_product(self):
		p_product=self.cleaned_data.get("p_product")
		try:
			p_id=int(p_product)
		except ValueError:
			forms.ValidationError("上级业务线错误")
		if p_id==0:
			return None
		try:
			p_obj=Product.objects.get(pk=p_id)
		except Product.DoesNotExist:
			forms.ValidationError("上级业务线不存在")

	def clean_op_interface(self):
		op_interface=self.cleaned_data.get("op_interface")
		return ",".join(op_interface)

	def clean_dev_inerface(self):
		op_interface=self.cleaned_data.get("op_interface")
		return ",".join(dev_interface)
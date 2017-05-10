#coding:utf8
from django import forms
class IdcForm(forms.Form):
	name=forms.CharField(required=True,max_length=10,error_messages={"required":"机房简称不能为空","max_length":"长度必须小于10"})
	idc_name=forms.CharField(required=True,max_length=100)
	address=forms.CharField(required=True,max_length=255)
	user=forms.CharField(required=True,max_length=32)
	user_phone=forms.CharField(required=True,max_length=20)
	user_email=forms.CharField(required=True,max_length=32)

	def clean_name(self):
		name=self.cleaned_data.get('name')
		return name.lower()
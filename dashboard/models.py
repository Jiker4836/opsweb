#coding:utf8
from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Server(models.Model):
	hostname=models.CharField(max_length=32,unique=True)
	ip=models.CharField(max_length=15,unique=True)
	cpu=models.CharField(max_length=50)
	mem=models.CharField(max_length=50)
	disk=models.CharField(max_length=50)
	sn=models.CharField(max_length=32)
	idc=models.CharField(max_length=50)
	ipinfo=models.CharField("[{'eth0':'192.168.1.1','mac':''},{'eth1':'192.168.1.1','mac':''}]",max_length=255)
	product=models.CharField(max_length=50)
	remark=models.TextField(default='')

	def __str__(self):
		return "{} {}".format(self.hostname,self.ip)

	class Meta:
		db_table='server'

class Department(models.Model):
	name=models.CharField(max_length=11,null=True)

	class Meta:
		db_table="department"

class Profile(models.Model):
	user=models.OneToOneField(User)
	phone=models.CharField(max_length=32,null=True)
	title=models.CharField(max_length=32,null=True)
	name=models.CharField("中文名",max_length=32,null=True)
	# department=models.CharField(max_length=32,null=True)
	department=models.ForeignKey(Department,null=True)

	class Meta:
		db_table="user_profile"
		default_related_name="profile"
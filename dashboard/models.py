#coding:utf8
from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Idc(models.Model):
	name=models.CharField('idc字母简称',max_length=10,unique=True)
	idc_name=models.CharField('idc中文名',max_length=100)
	address=models.CharField('idc地址',max_length=255)
	user=models.CharField('机房联系人',max_length=32)
	user_phone=models.CharField('机房联系人电话',max_length=20)
	user_email=models.EmailField('机房联系人邮箱',max_length=20)

	class Meta:
		db_table="idc"
		permissions=(
			("view_idc","查看idc"),
			)

class Server(models.Model):
    supplier        = models.IntegerField(null=True)
    manufacturers   = models.CharField(max_length=50, null=True)
    manufacture_date= models.DateField(null=True)
    server_type     = models.CharField(max_length=20, null=True)
    sn              = models.CharField(max_length=60, db_index=True, null=True)
    idc             = models.ForeignKey(Idc, null=True)
    os              = models.CharField(max_length=50, null=True)
    hostname        = models.CharField(max_length=50, db_index=True, null=True)
    inner_ip        = models.CharField(max_length=32, null=True, unique=True)
    mac_address     = models.CharField(max_length=50, null=True)
    ip_info         = models.CharField(max_length=255, null=True)
    server_cpu      = models.CharField(max_length=250, null=True)
    server_disk     = models.CharField(max_length=100, null=True)
    server_mem      = models.CharField(max_length=100, null=True)
    status          = models.CharField(max_length=100,db_index=True, null=True)
    remark          = models.TextField(null=True)
    #service_id      = models.IntegerField(db_index=True, null=True)
    #server_purpose  = models.ForeignKey(Product,null=True)
    check_update_time = models.DateTimeField(auto_now=True,null=True)
    vm_status       = models.IntegerField(db_index=True, null=True)
    uuid            = models.CharField(max_length=100, db_index=True,null=True)


    def __str__(self):
        return "{} {}".format(self.hostname, self.inner_ip)

    class Meta:
        db_table = "server"
        permissions = (
            ("view_server", "访问服务器信息"),
        )

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

class Status(models.Model):
    name=models.CharField("状态",max_length=32,unique=True)
    class Meta:
        db_table="status"

class Product(models.Model):
    name=models.CharField("业务线名称",max_length=32)
    p_product=models.ForeignKey("self",null=True,verbose_name='上级业务线')
    module_letter=models.CharField("业务线字母简称",max_length=10)
    op_interface=models.CharField("运维负责人：username1,username2",max_length=255)
    dev_interface=models.CharField("开发负责人：username1,username2",max_length=255)

    def __str__(self):
        return "{}".format(self.module_letter)

    class Meta:
        db_table="product"
        permissions=(
            ("view_product","管理业务线"),
            )

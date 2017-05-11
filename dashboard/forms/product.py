# coding: utf-8
from django import forms
from dashboard.models import Product
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404


class ProductForm(forms.Form):

    name            = forms.CharField(required=True, max_length=32,
                                       error_messages={"required": u"业务线名称不能为空", "max_length": "长度必须小于32"})

    p_product       = forms.CharField(required=True)

    module_letter   = forms.CharField(required=True, max_length=32,
                                      error_messages={"required": u"业务线简称不能为空", "max_length": "长度必须小于32"})
    # 多选，list
    choices_list    = ((user_obj.username, user_obj.email) for user_obj in User.objects.all())
    op_interface    = forms.MultipleChoiceField(choices=((user_obj.username, user_obj.email) for user_obj in User.objects.all()))
    dev_interface   = forms.MultipleChoiceField(choices=((user_obj.username, user_obj.email) for user_obj in User.objects.all()))

    def clean_module_letter(self):
        # 自定义字段验证  clean_字段名称
        # 获取name
        module_letter = self.cleaned_data.get("module_letter")
        # 处理转换为小写
        module_letter.strip().lower()
        return module_letter

    def clean_p_product(self):
        # 上级业务线：
        # 顶级业务线     0
        # 非顶级业务线   上级业务线 p_obj
        p_product = self.cleaned_data.get("p_product")
        try:
            # 整数类型校验
            p_id = int(p_product)
        except ValueError:
            forms.ValidationError("上级业务线错误")

        if p_product == "0":
            # 顶级业务线
            # p_product       = models.ForeignKey("self", null=True, verbose_name="上级业务线")
            # p_product 可以为null，所以要返回None，而不是空字符串。空字符串会包错：
            # (u'Cannot assign "\'\'": "Product.p_product" must be a "Product" instance.',)
            # return ""
            return None
        else:
            # 不是顶级业务线，p_product必须存在
            # get_object_or_404(Product, pk=p_product)
            try:
                p_obj = Product.objects.get(pk=p_id)
                print p_obj.name
                return p_obj
            except Product.DoesNotExist:
                forms.ValidationError("上级业务线不存在")

    def clean_op_interface(self):
        op_interface = self.cleaned_data.get("op_interface")
        print op_interface
        return ",".join(op_interface)

    def clean_dev_interface(self):
        dev_interface = self.cleaned_data.get("dev_interface")
        print dev_interface
        return ",".join(dev_interface)

    def clean(self):
        # 要先调用父类的方法
        super(ProductForm, self).clean()

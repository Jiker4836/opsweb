# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0013_idc'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='server',
            options={'permissions': (('view_server', '\u8bbf\u95ee\u670d\u52a1\u5668\u4fe1\u606f'),)},
        ),
        migrations.RemoveField(
            model_name='server',
            name='cpu',
        ),
        migrations.RemoveField(
            model_name='server',
            name='disk',
        ),
        migrations.RemoveField(
            model_name='server',
            name='ip',
        ),
        migrations.RemoveField(
            model_name='server',
            name='ipinfo',
        ),
        migrations.RemoveField(
            model_name='server',
            name='mem',
        ),
        migrations.RemoveField(
            model_name='server',
            name='product',
        ),
        migrations.AddField(
            model_name='server',
            name='check_update_time',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='server',
            name='inner_ip',
            field=models.CharField(max_length=32, unique=True, null=True),
        ),
        migrations.AddField(
            model_name='server',
            name='ip_info',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='server',
            name='mac_address',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='server',
            name='manufacture_date',
            field=models.DateField(null=True),
        ),
        migrations.AddField(
            model_name='server',
            name='manufacturers',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='server',
            name='os',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='server',
            name='server_cpu',
            field=models.CharField(max_length=250, null=True),
        ),
        migrations.AddField(
            model_name='server',
            name='server_disk',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='server',
            name='server_mem',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='server',
            name='server_type',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='server',
            name='status',
            field=models.CharField(max_length=100, null=True, db_index=True),
        ),
        migrations.AddField(
            model_name='server',
            name='supplier',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='server',
            name='uuid',
            field=models.CharField(max_length=100, null=True, db_index=True),
        ),
        migrations.AddField(
            model_name='server',
            name='vm_status',
            field=models.IntegerField(null=True, db_index=True),
        ),
        migrations.AlterField(
            model_name='server',
            name='hostname',
            field=models.CharField(max_length=50, null=True, db_index=True),
        ),
        migrations.AlterField(
            model_name='server',
            name='idc',
            field=models.ForeignKey(to='dashboard.Idc', null=True),
        ),
        migrations.AlterField(
            model_name='server',
            name='remark',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='server',
            name='sn',
            field=models.CharField(max_length=60, null=True, db_index=True),
        ),
    ]

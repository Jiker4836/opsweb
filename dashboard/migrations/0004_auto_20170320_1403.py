# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('dashboard', '0003_profle'),
    ]

    operations = [
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=11, null=True)),
            ],
            options={
                'db_table': 'department',
            },
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('phone', models.CharField(max_length=32, null=True)),
                ('title', models.CharField(max_length=32, null=True)),
                ('department', models.CharField(max_length=32, null=True)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'user_profile',
                'default_related_name': 'profile',
            },
        ),
        migrations.RemoveField(
            model_name='profle',
            name='user',
        ),
        migrations.DeleteModel(
            name='Profle',
        ),
    ]

# coding:utf-8
from dashboard.monitor.zabbix.zb import zb

def get_zabbix_groups():
    groups = zb.zb.hostgroup.get(output=["groupid","name"])
    return groups

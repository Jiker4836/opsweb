# coding:utf-8
from dashboard.monitor.zabbix.zb import zb
from dashboard.models import Server

def get_zabbix_groups():
    groups = zb.zb.hostgroup.get(output=["groupid","name"])
    return groups



def link_templates(serverids, templateids):
    data = []
    for serverid in serverids:
        ret_data = {}
        try:
            host = Server.objects.get(pk=serverid)
            ret_data['hostname'] = host.hostname
            ret = zb.link_template(host.zabbixhost.hostid, templateids)
        except Server.DoesNotExist:
            pass
        except AttributeError, e:
            ret_data['status'] = False
            ret_data["errmsg"] = "zabbix没有监控该主机"
        else:

            if "hostids" in ret:
                ret_data['status'] = True
            else:
                ret_data['status'] = False
                ret_data["errmsg"] = ret[0]
        data.append(ret_data)
    return data

def unlink_tempaltes(serverid, templateid):
    try:
        server = Server.objects.get(pk=serverid)
        hostid = server.zabbixhost.hostid
    except Server.DoesNotExist:
        raise Exception("服务器不存在")
    except AttributeError:
        raise Exception("请选同步缓存")
    ret = zb.unlink_template(hostid, templateid)
    if "hostids" in ret:
        return True
    raise Exception(ret[0])

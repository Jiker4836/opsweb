# coding:utf-8


from dashboard.models import Server, ZabbixHost
from dashboard.monitor.zabbix.zb import Zabbix, zb




def _create_host(hostname, ip, groupid='2', port="10050"):
    params = {
        "host": hostname,
        "interfaces": [
            {
                "type": 1,
                "main": 1,
                "useip": 1,
                "ip": ip,
                "dns": "",
                "port": port
            }
        ],
        "groups": [
            {
                "groupid": groupid
            }
        ]
    }
    try:
        ret = zb.create_hosts(params)
        if "hostids" in ret:
            if ret['hostids'][0].isdigit():
                return ret['hostids'][0]
            else:
                raise Exception(ret['hostids'][0])
    except Exception, e:
        raise Exception(e.args[0])



def create_host(serverids=[],groupid="2"):
    ret_data = []
    if isinstance(serverids, list) and serverids:
        servers = Server.objects.filter(pk__in=serverids)
        for server in servers:
            zb_data = {}
            zb_data['hostname'] = server.hostname
            try:
                hostid = _create_host(server.hostname,server.inner_ip, groupid)
                zb_data['status'] = True
            except Exception, e:
                zb_data['status'] = False
                zb_data['errmsg'] = e.args
            else:
                try:
                    zbhost = ZabbixHost()
                    zbhost.server = server
                    zbhost.hostid = hostid
                    zbhost.host = server.hostname
                    zbhost.ip = server.inner_ip
                    zbhost.save()
                except Exception, e:
                    zb_data['status'] = False
                    zb_data['errmsg'] = "同步成功，但缓存失败： {}".format(e.args)
            ret_data.append(zb_data)
    return ret_data



class ZabbixCacheHost(Zabbix):
    def __init__(self):
        super(ZabbixCacheHost, self).__init__()


    def cache_zabbix(self):
        ZabbixHost.objects.all().delete()
        hosts = self.get_hosts()
        zb_hosts_ids = [host.get('hostid') for host in hosts]
        zb_hosts_interface = self.get_interface(zb_hosts_ids)
        for host in hosts:
            try:
                zhost = ZabbixHost.objects.get(hostid__exact=host['hostid'])
                if not zbhost.server:
                    zbhost.server = self.get_server(zbhost.ip)
                zhost.save()
            except ZabbixHost.DoesNotExist:
                host['ip'] = zb_hosts_interface[host['hostid']]
                zbhost = ZabbixHost(**host)
                zbhost.server = self.get_server(zbhost.ip)
                zbhost.save()
        return True


    def get_server(self, ip):
        try:
            return Server.objects.get(inner_ip__exact=ip)
        except Server.DoesNotExist:
            return None


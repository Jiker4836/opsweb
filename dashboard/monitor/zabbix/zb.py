# coding:utf-8
import random
from zabbix_client import ZabbixServerProxy

from django.conf import settings
from dashboard.models import ZabbixHost, Server




class Zabbix(object):
    def __init__(self):
        self.zb = ZabbixServerProxy(settings.ZABBIX_URL)
        self.zb.user.login(user=settings.ZABBIX_USER, password=settings.ZABBIX_PASS)

    def get_hosts(self):
        return self.zb.host.get(output=['hostid', 'host'])

    def get_interface(self,ids):
        data = self.zb.hostinterface.get(hostids=ids, output=['hostid', 'ip'])
        ret = {}
        for d in data:
            ret[d['hostid']] = d['ip']
        return ret

    def get_hostgroup(self):
        data = self.zb.hostgroup.get(output=['groupid', 'name'])
        return data

    def get_template(self,ids=None):
        kwargs = {"output": ['templateid', 'name']}
        if ids:
            kwargs['hostids'] = ids
        ret = self.zb.template.get(**kwargs)
        return ret

    def link_template(self,hostid, templates):
        linked_templates_ids = [t['templateid'] for t in self.get_template(hostid)]
        linked_templates_ids.extend(templates)
        return self._link_template(hostid, linked_templates_ids)



    def _link_template(self, hostid, templateids):
        templates = []
        for id in templateids:
            templates.append({"templateid": id})
        try:
            ret = self.zb.host.update(hostid=str(hostid),templates=templates)
        except Exception as e:
            return e.args
        return ret

    def unlink_template(self, hostid, templateid):
        return self.zb.host.update(hostid= hostid,templates_clear=[{"templateid":templateid}])

    def create_hosts(self, params):
        return self.zb.host.create(**params)

    def create_maintenance(self, hostids, active_since, active_till):
        data = {'name':random.randint(1,100000),
                'active_since': active_since,
                'active_till': active_till,
                'hostids':hostids,
                'timeperiods':[
                        {
                            "timeperiod_type": 0,
                            "start_date":active_since,
                            "period":  active_till
                        }
                    ]
                }
        try:
            ret = self.zb.maintenance.create(data)
        except Exception as e:
            ret = {'error': e.args}
        return ret

    def del_maintenance(self, maintenanceids):
        return self.zb.maintenance.delete(maintenanceids)


    def get_maintenance(self):
        return self.zb.maintenance.get(output=['active_since','active_till','maintenanceid'],selectHosts=['name'])



    def rsync_zabbix_to_zbhost(self):
        """
            将zabbix里的监控主机同步到缓存表中
        :return:
        """
        zb_hosts = self.get_hosts()
        zb_hosts_ids = [zb.get('hostid') for zb in zb_hosts]
        zb_hosts_interface = self.get_interface(zb_hosts_ids)
        for host in zb_hosts:
            try:
                ZabbixHost.objects.get(hostid__exact=host['hostid'])
            except ZabbixHost.DoesNotExist:
                host['ip'] = zb_hosts_interface[host['hostid']]
                zbhost = ZabbixHost(**host)
                zbhost.save()

    def rsync_server_to_zbhost(self):
        """
            将服务器信息同步到缓存表中
        :return:
        """
        host = ZabbixHost.objects.all()
        servers = Server.objects.filter(inner_ip__in=[h.ip for h in host])
        servers_info = {}
        for s in servers:
            servers_info[s.inner_ip] = s.id

        host_not_in_cmdb = []
        for h in host:
            if not h.cmdb_hostid:
                try:
                    ZabbixHost.objects.filter(id__exact=h.id).update(cmdb_hostid=servers_info[h.ip])
                except KeyError:
                    host_not_in_cmdb.append(h.ip)

    def __del__(self):
        self.zb.user.logout()

zb = Zabbix()

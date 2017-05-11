# coding:utf-8

import json
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView, ListView, View
from django.http import HttpResponse, JsonResponse, QueryDict
from dashboard.models import ZabbixHost, Server
from dashboard.server.product import Ztree
from dashboard.monitor.zabbix.host import ZabbixCacheHost
from dashboard.monitor.zabbix.hostgroup import get_zabbix_groups
from dashboard.monitor.zabbix.host import create_host
from dashboard.monitor.zabbix.zb import zb
from dashboard.monitor.zabbix.template import link_templates, unlink_tempaltes

class HostRsyncView(ListView):

    http_method_names = ['get', 'post', 'put', 'patch', 'delete', 'head', 'options', 'trace', 'search', "async"]
    template_name = "monitor/zabbix/host_rsync.html"
    model = ZabbixHost

    def get_context_data(self, **kwargs):
        context = super(HostRsyncView, self).get_context_data(**kwargs)
        context['ztree'] = json.dumps(Ztree().get(async=True))
        context['groups'] = get_zabbix_groups()
        context['servers'] = Server.objects.values("id", "hostname")[0:10]
        return context

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        return super(HostRsyncView, self).get(request, *args, **kwargs)

    @method_decorator(login_required)
    def search(self, request):
        data = QueryDict(request.body)
        key = data.get('key', None)
        data = []
        if key is not None:
            data = Server.objects.filter(hostname__contains=key).values("id", "hostname")[:10]
        return JsonResponse(list(data), safe=False)

    @method_decorator(login_required)
    def post(self, request):
        ret = {"status": 0, "errmsg": ""}
        groupid = request.POST.get('group', None)
        serverids = request.POST.getlist("server", [])
        ret_data = create_host(serverids, groupid)
        ret['data'] = ret_data
        return JsonResponse(ret, safe=False)

    @method_decorator(login_required)
    def async(self, request):
        params = QueryDict(request.body)
        server_purpose = params.get("id")
        data = []
        try:

            for server in Server.objects.filter(server_purpose_id=server_purpose):
                z_data = {}
                z_data['id'] = server.id
                z_data['name'] = server.hostname
                z_data['open'] = True
                data.append(z_data)
        except Exception, e:
            pass
        return JsonResponse(data, safe=False)


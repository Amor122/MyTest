import logging

from django.http import JsonResponse, HttpRequest
from django.shortcuts import render

from human_management.models import Human, Organization, HumanPost


def show_organization(request):
    """欢迎页"""
    return render(request, 'show_organization.html', locals())


def show_organization2(request):
    """欢迎页"""
    return render(request, 'show_organization2.html', locals())


def get_organization_info(request):
    """为组织结构图分装数据的视图函数"""
    org_objs = Organization.objects.all()
    data_list = []
    for obj in org_objs:
        obj: Organization
        if obj.up_organization:
            up_org_id = ''.join(str(obj.up_organization.id).split('-'))
        else:
            up_org_id = '0'
        org_id = ''.join(str(obj.id).split('-'))
        org_name = obj.organization_name
        data_dict = {
            'subcompanyname': org_name,
            'supsubcomid': up_org_id,
            'id': org_id,
        }
        data_list.append(data_dict)
    print(data_list)
    return JsonResponse(data={
        'status': True,
        'data_list': data_list,
        'message': '成功加载组织数据，正在绘制组织结构图形',
    }, safe=False, json_dumps_params={'ensure_ascii': False})


def get_organization_dict_info(request):
    """为组织结构图分装数据的视图函数"""
    org_objs = Organization.objects.all()
    # 直接读这个反向查询有问题，所以直接构建新数据
    data_dict = {}
    start_org = []
    for obj in org_objs:
        if not obj.up_organization:
            start_org.append(obj.organization_name)
        # print(obj.down_organization.all())
        obj: Organization
        obj_name = obj.organization_name
        if obj.up_organization:
            up_name = obj.up_organization.organization_name
        else:
            up_name = ''
        if obj_name not in data_dict:
            data_dict.update({obj_name: []})
        else:
            pass
        if up_name:
            if up_name not in data_dict:
                data_dict.update({up_name: []})
            if obj_name not in data_dict[up_name]:
                data_dict[up_name].append(obj_name)
    print(data_dict)

    return JsonResponse(data={
        'status': True,
        'message': '成功加载组织数据，正在绘制组织结构图形',
        'data_list': data_dict,
        'start_org': start_org,
    }, safe=False, json_dumps_params={'ensure_ascii': False})

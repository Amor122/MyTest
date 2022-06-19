import logging

from django.http import JsonResponse, HttpRequest
from django.shortcuts import render

from human_management.models import Human, Organization, HumanPost, OrganizationType


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


def get_organization_by_name(request):
    org_name = request.POST.get('org_name')
    print(org_name)
    if org_name:
        obj: Organization = Organization.objects.filter(organization_name=org_name).first()
        if obj:
            data_dict = {
                'organization_id': obj.id,
                'organization_name': obj.organization_name,
                'organization_type': obj.organization_type.organization_type_name if obj.organization_type else '',
                'up_organization': obj.up_organization.organization_name if obj.up_organization else '',
            }
            organization_list_objs = Organization.objects.all().exclude(organization_name=obj.organization_name)
            organization_list = []
            for list_obj in organization_list_objs:
                list_obj: Organization
                organization_list.append(list_obj.organization_name)

            organization_type_objs = OrganizationType.objects.all()
            organization_type_list = []
            for list_obj in organization_type_objs:
                list_obj: OrganizationType
                organization_type_list.append(list_obj.organization_type_name)

            return JsonResponse(data={
                'status': True,
                'data_dict': data_dict,
                'organization_list': organization_list,
                'organization_type_list': organization_type_list,
                'message': f'加载组织{obj.organization_name}信息成功',
            }, safe=False, json_dumps_params={'ensure_ascii': False})

    return JsonResponse(data={
        'status': False,
        'message': f'数据加载错误',
    }, safe=False, json_dumps_params={'ensure_ascii': False})


def delete_organization_by_id(request):
    organization_id = request.POST.get('organization_id')

    if organization_id:
        obj: Organization = Organization.objects.get(pk=organization_id)
        if obj:
            # 删除前重新连接链路
            up_org = obj.up_organization
            down_orgs = obj.down_organization.all()
            for down_org in down_orgs:
                down_org.up_organization = up_org
                down_org.save()

            obj.delete()

            return JsonResponse(data={
                'status': True,
                'message': f'删除组织{obj.organization_name}信息成功',
            }, safe=False, json_dumps_params={'ensure_ascii': False})

    return JsonResponse(data={
        'status': False,
        'message': f'数据加载错误',
    }, safe=False, json_dumps_params={'ensure_ascii': False})


def edit_organization_by_id(request):
    organization_id = request.POST.get('organization_id')
    organization_name = request.POST.get('organization_name')
    organization_type = request.POST.get('organization_type')
    up_organization = request.POST.get('up_organization')
    org_obj: Organization = Organization.objects.get(pk=organization_id)
    org_type_obj = OrganizationType.objects.filter(organization_type_name=organization_type).first()
    up_org_obj = Organization.objects.filter(organization_name=up_organization).first()
    if organization_type == '------':
        org_type_obj = None
    if up_organization == '------':
        up_org_obj = None

    if all((org_obj, organization_name)):
        old_organization_name = org_obj.organization_name
        org_obj.organization_name = organization_name
        org_obj.organization_type = org_type_obj
        org_obj.up_organization = up_org_obj
        org_obj.save()
        return JsonResponse(data={
            'status': True,
            'message': f'修改组织{old_organization_name}信息成功',
        }, safe=False, json_dumps_params={'ensure_ascii': False})

    return JsonResponse(data={
        'status': False,
        'message': f'数据加载错误',
    }, safe=False, json_dumps_params={'ensure_ascii': False})


def add_organization(request):
    if request.method == 'POST':
        organization_name = request.POST.get('organization_name')
        organization_type = request.POST.get('organization_type')
        up_organization = request.POST.get('up_organization')
        org_obj: Organization = Organization.objects.filter(organization_name=organization_name).first()

        org_type_obj = OrganizationType.objects.filter(organization_type_name=organization_type).first()
        up_org_obj = Organization.objects.filter(organization_name=up_organization).first()
        if organization_type == '------':
            org_type_obj = None
        if up_organization == '------':
            up_org_obj = None
        if not org_obj:
            org_obj = Organization()
            org_obj.organization_name = organization_name
            org_obj.organization_type = org_type_obj
            org_obj.up_organization = up_org_obj
            org_obj.save()
            return JsonResponse(data={
                'status': True,
                'message': f'添加组织{organization_name}信息成功',
            }, safe=False, json_dumps_params={'ensure_ascii': False})
        else:
            return JsonResponse(data={
                'status': False,
                'message': f'组织名称重复',
            }, safe=False, json_dumps_params={'ensure_ascii': False})
    return JsonResponse(data={
        'status': False,
        'message': f'数据加载错误',
    }, safe=False, json_dumps_params={'ensure_ascii': False})


def get_organization_types(requests):
    organization_type_objs = OrganizationType.objects.all()
    organization_type_list = []
    for obj in organization_type_objs:
        organization_type_list.append(obj.organization_type_name)
    return JsonResponse(data={
        'organization_type_list': organization_type_list
    }, safe=False, json_dumps_params={'ensure_ascii': False})

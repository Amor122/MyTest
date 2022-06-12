import logging

from django.db import IntegrityError
from django.http import JsonResponse, HttpRequest
from django.shortcuts import render

from human_management.models import Human, Organization, HumanPost
from .tools import human_management_decorate


def log_handler(request, human_obj, handle_type):
    """
    定义一个常规的人员模型操作记录器。
    :param request: 请求数据
    :param human_obj: 人员模型
    :param handle_type: 操作类型
    :return: 不返回
    """
    # 工号、姓名、操作、什么数据
    message = 'USER_ID:{} -- NAME:{} -- {} -- {}'
    login_user = request.session.get('login_user')
    user_id = None
    user_name = None
    if login_user:
        user_id = login_user.get('user_id')
        user_name = login_user.get('user_name')
    user_id = user_id if user_id else '未登录'
    user_name = user_name if user_name else '未登录'
    information = f'{human_obj.user_id}:{human_obj.user_name}'
    msg = message.format(user_id, user_name, handle_type, information)
    logging.getLogger('my_log').info(msg)


def test_view(request):
    return render(request, 'index.html', locals())


def show_human(request):
    """显示人员管理界面"""
    return render(request, 'show_human.html', locals())


def get_human(request):
    data_list = []
    objs = Human.objects.all()
    for obj in objs:
        obj: Human
        if obj.post:
            post = obj.post.post_name
            chief = obj.post.is_primary
        else:
            post = '无'
            chief = False

        if obj.organization:
            organization = obj.organization.organization_name
        else:
            organization = '无'
        data_dict = {
            'id': obj.id,
            'organization': organization,
            'user_id': obj.user_id,
            'user_name': obj.user_name,
            'post': post,
            'chief': chief,
        }
        data_list.append(data_dict)
    print(data_list)

    return JsonResponse(data=data_list, safe=False)


@human_management_decorate
def edit_human(request):
    print(request.method)
    if request.method == 'POST':
        id = request.POST.get('id')
        user_name = request.POST.get('user_name')
        user_id = request.POST.get('user_id')
        organization = request.POST.get('organization')
        post = request.POST.get('post')
        human_obj: Human = Human.objects.get(pk=id)
        print(id, user_id, user_name, organization, post)
        organization_obj = Organization.objects.filter(organization_name=organization).first()
        post_obj = HumanPost.objects.filter(post_name=post).first()
        if all((human_obj, organization_obj, post_obj)):
            human_obj.user_name = user_name
            human_obj.user_id = user_id
            human_obj.post = post_obj
            human_obj.organization = organization_obj
            update_status = False
            try:
                human_obj.save()
                log_handler(request, human_obj, 'edit')
                print('修改成功')
                update_status = True
            except IntegrityError as e:
                print('修改失败', e)
                update_status = False
            return JsonResponse(data={
                'status': update_status
            }, safe=False)
        else:
            return JsonResponse(data={
                'status': False
            }, safe=False)

    return JsonResponse(data={
        'status': False,
        'message': 'method not allowed'
    }, safe=False)


@human_management_decorate
def add_human(request):
    print(request.method)
    if request.method == 'POST':
        user_name = request.POST.get('user_name')
        user_id = request.POST.get('user_id')
        organization = request.POST.get('organization')
        post = request.POST.get('post')
        human_obj: Human = Human()
        print(id, user_id, user_name, organization, post)
        organization_obj = Organization.objects.filter(organization_name=organization).first()
        post_obj = HumanPost.objects.filter(post_name=post).first()
        if all((organization_obj, post_obj)):
            human_obj.user_name = user_name
            human_obj.user_id = user_id
            human_obj.post = post_obj
            human_obj.organization = organization_obj
            update_status = False
            try:
                human_obj.save()
                log_handler(request, human_obj, 'add')
                print('修改成功')
                update_status = True
            except IntegrityError as e:
                print('修改失败', e)
                update_status = False
            return JsonResponse(data={
                'status': update_status
            }, safe=False)
        else:
            return JsonResponse(data={
                'status': False
            }, safe=False)

    return JsonResponse(data={
        'status': False,
        'message': 'method not allowed'
    }, safe=False)


def get_organizations(requests):
    organization_objs = Organization.objects.all()
    organization_list = []
    for obj in organization_objs:
        organization_list.append(obj.organization_name)
    return JsonResponse(data={
        'organization_list': organization_list
    }, safe=False, json_dumps_params={'ensure_ascii': False})


def get_posts(requests):
    post_objs = HumanPost.objects.all()
    post_list = []
    for obj in post_objs:
        post_list.append(obj.post_name)
    return JsonResponse(data={
        'post_list': post_list
    }, safe=False, json_dumps_params={'ensure_ascii': False})


@human_management_decorate
def reset_user_password(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        if not id:
            return JsonResponse(data={
                'status': False,
                'message': 'id not found'
            }, safe=False)

        human_obj: Human = Human.objects.get(pk=id)
        default_password = 'abc123456'
        if human_obj:
            log_handler(request, human_obj, 'reset_password')
            human_obj.password = default_password
            human_obj.save()
            print(f'密码重置成功，重置为:{default_password}')
            return JsonResponse(data={
                'status': True,
                'message': f'密码重置成功，重置为:{default_password}'
            }, safe=False)
        return JsonResponse(data={
            'status': False
        }, safe=False)

    else:
        return JsonResponse(data={
            'status': False,
            'message': 'method not allowed'
        }, safe=False)


@human_management_decorate
def delete_user_by_id(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        if not id:
            return JsonResponse(data={
                'status': False,
                'message': 'id not found'
            }, safe=False)
        human_obj: Human = Human.objects.get(pk=id)
        if human_obj:
            log_handler(request, human_obj, 'delete')
            human_obj.delete()
            return JsonResponse(data={
                'status': True,
                'message': f'用户删除成功'
            }, safe=False)
        return JsonResponse(data={
            'status': True
        }, safe=False)

    else:
        return JsonResponse(data={
            'status': False,
            'message': 'method not allowed'
        }, safe=False)

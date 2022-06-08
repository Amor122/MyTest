from django.http import JsonResponse
from django.shortcuts import render

from human_management.models import Human


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

    return JsonResponse(data=data_list,safe=False)

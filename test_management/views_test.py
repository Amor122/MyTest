import datetime
import logging

from django.http import JsonResponse, HttpRequest
from django.shortcuts import render

from human_management.models import Human, Organization, HumanPost, OrganizationType
from .models import Test, Difficulty, Subject


def show_test(request):
    """欢迎页"""
    return render(request, 'show_test.html', locals())


def get_test(request):
    test_objs = Test.objects.all().filter(delete_status=False).order_by('-start_time')
    data_list = []
    for obj in test_objs:
        obj: Test
        data_dict = {
            'id': obj.id,
            'subject': obj.subject.subject_name if obj.subject else '',
            'difficulty': obj.difficulty.difficulty_name if obj.difficulty else '',
            'test_name': obj.test_name,
            'start_time': obj.start_time.strftime("%Y-%m-%d %H:%M"),
            # 'start_time': str(int(obj.start_time.timestamp()*1000)),
            'duration': obj.duration,
        }
        data_list.append(data_dict)
    print(data_list)
    return JsonResponse(data=data_list, safe=False, json_dumps_params={'ensure_ascii': False})


def delete_test_by_id(request):
    test_id = request.POST.get('test_id')

    if test_id:
        obj: Test = Test.objects.get(pk=test_id)
        if obj:
            # 删除实际是标记为删除，没有真的去除。
            obj.delete_status=True
            obj.save()

            return JsonResponse(data={
                'status': True,
                'message': f'删除考试：{obj.test_name}信息成功',
            }, safe=False, json_dumps_params={'ensure_ascii': False})

    return JsonResponse(data={
        'status': False,
        'message': f'数据加载错误',
    }, safe=False, json_dumps_params={'ensure_ascii': False})


def get_test_selections(request):
    difficulty_objs = Difficulty.objects.all()
    difficulties = []
    for obj in difficulty_objs:
        obj: Difficulty
        difficulties.append(obj.difficulty_name)

    subject_objs = Subject.objects.all()
    subjects = []
    for obj in subject_objs:
        obj: Subject
        subjects.append(obj.subject_name)
    return JsonResponse(data={
        'status': True,
        'message': '下拉选项数据加载成功',
        'difficulties': difficulties,
        'subjects': subjects,
    }, safe=False, json_dumps_params={'ensure_ascii': False})

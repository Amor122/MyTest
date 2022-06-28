import datetime
import logging

from django.http import JsonResponse, HttpRequest
from django.shortcuts import render

from human_management.models import Human, Organization, HumanPost, OrganizationType
from .models import Test, Difficulty, Subject, Invigilator


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
            obj.delete_status = True
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


def edit_test_by_id(request):
    test_id = request.POST.get('test_id')
    test_name = request.POST.get('test_name')
    difficulty = request.POST.get('difficulty')
    subject = request.POST.get('subject')
    duration = request.POST.get('duration')
    start_time = request.POST.get('start_time')
    test_obj: Test = Test.objects.get(pk=test_id)
    difficulty_obj: Difficulty = Difficulty.objects.filter(difficulty_name=difficulty).first()
    subject_obj: Subject = Subject.objects.filter(subject_name=subject).first()
    start_time = start_time.replace('T', ' ')
    try:
        st = datetime.datetime.strptime(start_time, '%Y-%m-%d %H:%M')
    except Exception as e:
        print(e)
        st = None

    if all((test_obj, difficulty_obj, subject_obj, test_name, duration, st)):
        old_test_name = test_obj.test_name
        test_obj.test_name = test_name
        test_obj.start_time = st
        test_obj.difficulty = difficulty_obj
        test_obj.subject = subject_obj
        test_obj.duration = duration
        test_obj.save()
        return JsonResponse(data={
            'status': True,
            'message': f'修改考试{old_test_name}信息成功',
        }, safe=False, json_dumps_params={'ensure_ascii': False})

    return JsonResponse(data={
        'status': False,
        'message': f'数据加载错误',
    }, safe=False, json_dumps_params={'ensure_ascii': False})


def add_test(request):
    if request.method == 'POST':
        test_name = request.POST.get('test_name_add')
        difficulty = request.POST.get('difficulty_add')
        subject= request.POST.get('subject_add')
        start_time = request.POST.get('start_time_add')
        duration= request.POST.get('duration_add')
        difficulty_obj: Difficulty = Difficulty.objects.filter(difficulty_name=difficulty).first()
        subject_obj: Subject = Subject.objects.filter(subject_name=subject).first()
        start_time = start_time.replace('T', ' ')
        try:
            st = datetime.datetime.strptime(start_time, '%Y-%m-%d %H:%M')
        except Exception as e:
            print(e)
            st = None

        if all((difficulty_obj, subject_obj, test_name, duration, st)):
            test_obj = Test()
            test_obj.test_name = test_name
            test_obj.start_time = st
            test_obj.difficulty = difficulty_obj
            test_obj.subject = subject_obj
            test_obj.duration = duration
            test_obj.save()
            return JsonResponse(data={
                    'status': True,
                    'message': f'添加考试{test_name}信息成功',
                }, safe=False, json_dumps_params={'ensure_ascii': False})
        else:
            return JsonResponse(data={
                'status': False,
                'message': f'信息错误，无法添加',
            }, safe=False, json_dumps_params={'ensure_ascii': False})
    return JsonResponse(data={
        'status': False,
        'message': f'数据加载错误',
    }, safe=False, json_dumps_params={'ensure_ascii': False})


def get_people(request,test_id):
    """监考人信息"""
    invigilator_objs = Invigilator.objects.all().filter(test__id=test_id)
    data_list = []
    for obj in invigilator_objs:
        obj: Invigilator
        data_dict = {
            'id': obj.id,
            'test_id': obj.test.id,
            'invigilator_id': obj.invigilator.user_id,
            'invigilator_name': obj.invigilator.user_name,
            'location': obj.location,
        }
        data_list.append(data_dict)
    print(data_list)
    return JsonResponse(data=data_list, safe=False, json_dumps_params={'ensure_ascii': False})

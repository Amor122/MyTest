import uuid

from django.contrib.auth.hashers import check_password
from django.http import HttpResponseRedirect
from django.shortcuts import render

from .models import Human


def management_login(request):
    return render(request, 'management_login.html', locals())


def management_login_handle(request):
    error_msg = ''
    if request.method == 'POST':
        account = request.POST.get('account', None)
        password = request.POST.get('password', None)

        if not all((account, password)):
            error_msg = '用户名密码不能为空'
        else:
            user_set = Human.objects.filter(user_id=account)
            if user_set.exists():
                user1: Human = user_set.first()
                check_label = False
                if check_password(password, user1.password):
                    if user1.organization:
                        if user1.organization.organization_type:
                            if not user1.organization.organization_type.organization_type_name.startswith('学生'):
                                check_label = True
                    if not check_label:
                        error_msg = ' 账号无登录权限'
                    else:
                        request.session['login_user'] = {
                            'user_name': user1.user_name,
                            'user_id': user1.user_id,
                        }
                        error_msg = ' 成功登录'
                        login_source = request.META['REMOTE_ADDR']

                        print(login_source)
                        response = HttpResponseRedirect('management_welcome')  # 这里留着以后转到其他页面
                        token = uuid.uuid4().hex
                        response.set_cookie('login_token', token, max_age=2000)
                        return response
                else:
                    error_msg = '用户密码错误，如忘记，请联系管理员'
            else:
                error_msg = '用户名不存在，请先联系管理员'

    return render(request, 'management_login.html', locals())


def management_login_out(request):
    """注销登录"""
    response = HttpResponseRedirect('management_login')

    if request.COOKIES.get('login_token'):
        response.delete_cookie('login_token')
    if request.session.get('login_user'):
        del request.session['login_user']
    if request.COOKIES.get('login_token'):
        del request.COOKIES['login_token']
        print('删除了cookie')
    return response


def management_welcome(request):
    """欢迎页"""
    return render(request, 'management_welcome.html', locals())


def testpage(request):
    """欢迎页"""
    return render(request, 'test_page.html', locals())

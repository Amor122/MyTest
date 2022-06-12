"""这里是部分功能的权限判断装饰器"""
from django.http import JsonResponse

from human_management.models import Human


def human_management_decorate(func):
    def new_func(request):
        error_response = JsonResponse(data={
            'status': False,
            'message': '登录信息校验失败，请重新登录！'
        }, safe=False)
        warning_response = JsonResponse(data={
            'status': False,
            'message': '您不具有操作数据的权限，请联系管理员处理，页面仅提供查看'
        }, safe=False)
        login_user = request.session.get('login_user')
        if not login_user:
            return error_response
        else:
            user_id = login_user.get('user_id')
            user_name = login_user.get('user_name')
            if not all((user_id, user_name)):
                return error_response
            else:
                user_obj = Human.objects.filter(user_id=user_id, user_name=user_name).first()
                if not user_obj:
                    return error_response
                else:
                    if user_obj.post:
                        post_name = user_obj.post.post_name
                        if post_name == '信息系统管理员':
                            # 这里标识通过校验，可以执行修改操作
                            # 执行被装饰的函数
                            print('通过校验')
                            return func(request)

                        else:
                            return warning_response
                    else:
                        return warning_response

    return new_func

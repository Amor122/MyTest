from django.http import HttpResponse, HttpResponseRedirect
from django.utils.deprecation import MiddlewareMixin


class LoginCheckMiddleware(MiddlewareMixin):
    def process_request(self, request):
        print('login_checkMiddleware,request', request.path, request.META['REMOTE_ADDR'])
        exclude_list = ['login', 'static']
        if 'human_management' not in request.path:
            pass
        elif 'admin' in request.path:
            pass
        elif 'login' in request.path:
            pass
        else:
            # 验证 用户是否已经登录
            if not request.COOKIES.get('login_token'):
                return HttpResponseRedirect('/human_management/management_login')

    def process_view(self, request, callback, callback_args, callback_kwargs):
        print('login_checkMiddleware,view')

    def process_response(self, request, response):
        print('login_checkMiddleware,response')
        return response

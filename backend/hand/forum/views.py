"""
引用的順序 原本的套件、django的套件、本地內的引用
"""
import datetime
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import get_authorization_header

from reg.forms import LoginForm
from reg.models import UserIfm
from reg.views import decode_access_token
from ifm.models import UserDefIfm
from forum.models import Discuss, DiscussResponse

from hand.settings import ROOT_EMAIL, NGINX_DOMAIN

# Create your views here.
# ------------------------- root驗證裝飾器 ------------------------------
def root_check(func):
    """
    登入確認，如果沒有找到登入的COOKIES會自度跳轉到登入的頁面。
    """
    def wrapper(req, request):
        print("request:",request, "\nreq:", req)

        token = request.COOKIES.get('access_token')

        if not token:
            form = LoginForm()
            payload = {
                "form" : form,
                "msg" : "請先登入後再執行該操作。"
            }
            response = Response(status=status.HTTP_202_ACCEPTED)
            html = render(request, 'login.html', payload).content.decode('utf-8')
            response.content = html
            return response

        user = decode_access_token(token)['id']
        instance = UserIfm.objects.get(email=ROOT_EMAIL)
        root_id = instance.id
        if user == root_id:
            result = func(req, request)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN, data = "權限不足")
        return result
    return wrapper
# ------------------------- root驗證裝飾器 ------------------------------

class ForumSendAPIView(APIView):
    """
    有登入帳號就可以使用發布文章的功能。
    """
    @swagger_auto_schema(
        operation_summary='送出文章',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'title' : openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description='文章標題'
                ),
                'content' : openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description='文章內容'
                )
            }
        )
    )

    def post(self, request): # pylint: disable=unused-argument
        """
        送出輸入的文字
        """
        auth = get_authorization_header(request).split()
        try:
            if auth[1] == b'null':
                data = {
                    'message' : '沒有token。'
                }
                response = JsonResponse(data, status=status.HTTP_401_UNAUTHORIZED)
                return response
        except IndexError as error_msg:
            print(error_msg)
            data = {
                'message' : '沒有header。'
            }
            response = JsonResponse(data, status=status.HTTP_401_UNAUTHORIZED)
            return response
        token = auth[1]
        instance = Discuss()
        user_id = decode_access_token(token)['id']
        user_instance = UserIfm.objects.get(id = user_id)
        instance.user = user_instance
        instance.content = request.data['content']
        instance.title = request.data['contentTitle']
        instance.upload_date = str(datetime.date.today())
        instance.save()
        page_id = Discuss.objects.filter(user_id=user_id).latest('id').id
        data = {
            'message':'成功發佈文章',
            'push' : f'/forum/{page_id}'
        }
        response = JsonResponse(data, status=status.HTTP_200_OK)
        return response

class ForumAPIView(APIView):
    """
    所有人都可以閱讀討論區
    """
    @swagger_auto_schema(
        operation_summary='列出討論區所有內容',
    )

    def get(self, resquest):    # pylint: disable=unused-argument
        """
        獲得發送的頁面。
        """
        instance = Discuss.objects.all()
        diec = {}
        for i in instance:
            diec[i.id] = i.title
        data = {
            'title' : diec,
        }
        response = JsonResponse(data, status=status.HTTP_200_OK)
        return response

class ForumArticalAPIView(APIView):
    """
    有登入可以使用查看所有討論的功能。
    """
    @swagger_auto_schema(
        operation_summary='列出討論區詳細內容',
    )

    def get(self, request, artical_id):
        """
        獲得發送的頁面。
        """
        instance = Discuss.objects.get(id=artical_id)
        author = instance.user.id   # 獲得該文章使用者的 userid
        author_name = UserIfm.objects.get(id=author).username
        user_instance = UserDefIfm.objects.get(user_id = author)
        author_headimage_url = f'{NGINX_DOMAIN}/api/ifm{user_instance.headimg.url}'  # 獲得文章作者的頭像
        response = DiscussResponse.objects.filter(dis_id=artical_id)    # 獲得該頁面所有回復

        response_list_name = ['id', 'response', 'upload_date']
        response_diec = {}
        response_person = {}
        for i in response:

            for name in response_list_name:
                response_person[name] = getattr(i, name)

            try:
                userdef_instance = UserDefIfm.objects.get(user_id = i.user_id.id)
                response_person['headimagUrl'] = f'{NGINX_DOMAIN}/api/ifm{userdef_instance.headimg.url}'
                response_person['username'] = i.user_id.username
            except AttributeError as error_msg:
                print(error_msg, 'ForumArticalAPIView')
                userdef_instance = UserDefIfm.objects.get(user_id = 80928899)   # 預設頭貼
                response_person['headimagUrl'] = f'{NGINX_DOMAIN}/api/ifm{userdef_instance.headimg.url}'
                response_person['username'] = '帳戶已刪除'

            response_diec[i.id] = response_person
            response_person = {}

        print(response_diec)    # 該頁面所有使用者個回復

        data = {
            'message' : '請求成功',
            'articalTitle' : instance.title,
            'authorname' : author_name,
            'authorImageUrl' : author_headimage_url,
            'articalContent' : instance.content,
            'uploadDate' : instance.upload_date,
            'response' : response_diec
        }
        print(data)
        response = JsonResponse(data, status=status.HTTP_200_OK)
        return response


    @swagger_auto_schema(
        operation_summary='送出留言',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'response' : openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description='回覆內容'
                ),
            }
        )
    )
    def post(self, request, artical_id):
        """
        使用者回覆留言
        """
        auth = get_authorization_header(request).split()
        try:
            if auth[1] == b'null':
                data = {
                    'message' : '沒有token。'
                }
                response = JsonResponse(data, status=status.HTTP_401_UNAUTHORIZED)
                return response
        except IndexError as error_msg:
            print(error_msg)
            data = {
                'message' : '沒有header。'
            }
            response = JsonResponse(data, status=status.HTTP_401_UNAUTHORIZED)
            return response
        token = auth[1]
        payload = decode_access_token(token=token)
        print(request, artical_id, 'addr', request.META['REMOTE_ADDR'])
        instance = DiscussResponse()
        user_instance = UserIfm.objects.get(id = payload['id'])
        discuss_instance = Discuss.objects.get(id = artical_id)

        instance.user_id = user_instance
        instance.response = request.data['userResponse']
        instance.dis_id = discuss_instance
        instance.upload_date = str(datetime.date.today())
        instance.save()
        data = {
            'message': '發送留言成功',
        }
        response = JsonResponse(data, status=status.HTTP_200_OK)

        return response

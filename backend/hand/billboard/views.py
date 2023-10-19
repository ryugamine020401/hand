"""
引用的順序 原本的套件、django的套件、本地內的引用
"""
import datetime
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import get_authorization_header
from rest_framework import status

from reg.models import UserIfm
from reg.forms import LoginForm
from reg.views import decode_access_token
from billboard.forms import BillboardForm
from billboard.models import Billboard

from hand.settings import ROOT_EMAIL

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

class RootCheckAPIView(APIView):
    """
    驗證使用者的權限
    """
    def post(self, request):
        auth = get_authorization_header(request).split()

        try:
            token = auth[1]
            if token == b'null':
                data = {
                    'message' : '找不到token'
                }
                response = JsonResponse(data, status=status.HTTP_404_NOT_FOUND)
                return response
        except IndexError as error_msg:
            print('RootCheckAPIView', error_msg)
            data = {
                'message' : '沒有Authorization'
            }
            response = JsonResponse(data, status=status.HTTP_400_BAD_REQUEST)
            return response
        token_payload = decode_access_token(token)
        if (ROOT_EMAIL == token_payload['email']):
            print("權限足夠")
            data = {
                'message' : '權限足夠',
            }
            response = JsonResponse(data, status=status.HTTP_200_OK)
            return response
        else:
            data = {
                'message' : '權限不足',
            }
            response = JsonResponse(data, status=status.HTTP_403_FORBIDDEN)
            return response

class BillboardSendAPIView(APIView):
    """
    有root權限可以使用發布公告的功能。
    """
    
    @swagger_auto_schema(
        operation_summary='root 發送公告',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'title' : openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description='公告標題'
                ),
                'content' : openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description='公告內容'
                ),
            }
        )
    )
    # @root_check
    def post(self, request):
        """
        送出輸入的文字
        """
        print(request)
        auth = get_authorization_header(request).split()
        try:
            if auth[1] == b'null':
                data = {
                    'message':'沒有token',
                }
                response = JsonResponse(data, status=status.HTTP_401_UNAUTHORIZED)
                return response
        except IndexError as error_msg:
            print(error_msg, 'BillboardSendAPIView')
            data = {
                'message':'沒有Authorization',
            }
            response = JsonResponse(data, status=status.HTTP_401_UNAUTHORIZED)
            return response

        instance = Billboard()
        instance.title = request.data['title']
        instance.content = request.data['content']
        instance.upload_date = str(datetime.date.today())
        instance.save()
        data = {
            'message':'發佈成功',
        }
        response = JsonResponse(data, status=status.HTTP_200_OK)
        return Response("發佈成功")

class BillboardView(APIView):
    """
    檢視所有公告內容
    """
    @swagger_auto_schema(
        operation_summary='所有公告內容',
    )
    def get(self, request):
        """
        獲得發送的頁面。
        """
        instance = Billboard.objects.all()
        diec = {}
        for i in instance:
            diec[i.id] = i.title
        data = {
            'title' : diec,
        }
        response = JsonResponse(data, status=status.HTTP_200_OK)
        return response

class BillboardArticalView(APIView):
    """
    所有人都可以閱讀布告欄
    """
    @swagger_auto_schema(
        operation_summary='獲取詳細頁面',
    )
    def get(self, request, artical_id):
        """
        獲得發送的頁面。
        """
        print(artical_id)
        try:
            instance = Billboard.objects.get(id=artical_id)
        except Billboard.DoesNotExist as errer_msg: # pylint: disable=E1101
            print(errer_msg, request)
            data = {
                "message" : '無此資源',
                "redirect" : '/billboard'
            }
            response = JsonResponse(data, status=status.HTTP_302_FOUND)
            return response
        data = {
            "message" : '成功獲取',
            "title" : instance.title,
            "content" : instance.content,
            "date" : instance.upload_date,
        }
        response = JsonResponse(data, status=status.HTTP_200_OK)
        return response

    def delete(self, request, artical_id):
        """
        root權限刪除文章。
        """
        try:
            auth = get_authorization_header(request).split()
            print(auth[1])
            if decode_access_token(auth[1])['email'] != ROOT_EMAIL:
                data = {
                "message" : '刪除失敗，權限不足',
                }
                response = JsonResponse(data, status=status.HTTP_403_FORBIDDEN)
                return response
        except IndexError as error_msg:
            print(error_msg)
            data = {
                "message" : '刪除失敗，權限不足',
            }
            response = JsonResponse(data, status=status.HTTP_403_FORBIDDEN)
            return response
        data = {
            "message" : '刪除成功',
        }
        Billboard.objects.get(id=artical_id).delete()
        response = JsonResponse(data, status=status.HTTP_200_OK)
        return response

"""
引用的順序 原本的套件、django的套件、本地內的引用
"""
import datetime

from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
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


class BillboardSendView(APIView):
    """
    有root權限可以使用發布公告的功能。
    """
    @root_check
    def get(self, request):
        """
        獲得發送的頁面。
        """
        form = BillboardForm()
        payload = {
            "form" : form,
        }
        response = Response(status=status.HTTP_202_ACCEPTED)
        html = render(request, 'billboardsend.html', payload).content.decode('utf-8')
        response.content = html
        return response
    @root_check
    def post(self, request):
        """
        送出輸入的文字
        """
        instance = Billboard()
        instance.title = request.data['title']
        instance.content = request.data['content']
        instance.upload_date = str(datetime.date.today())
        instance.save()

        return Response("發佈成功")

class BillboardView(APIView):
    """
    有root權限可以使用發布公告的功能。
    """
    def get(self, request):
        """
        獲得發送的頁面。
        """
        instance = Billboard.objects.all()
        payload = {
            "instance" : instance,
        }
        response = Response(status=status.HTTP_200_OK)
        html = render(request, 'billboard.html', payload).content.decode('utf-8')
        response.content = html
        return response

class BillboardArticalView(APIView):
    """
    所有人都可以閱讀布告欄
    """
    def get(self, request, artical_id):
        """
        獲得發送的頁面。
        """
        instance = Billboard.objects.get(id=artical_id)
        payload = {
            "instance" : instance,
        }
        response = Response(status=status.HTTP_200_OK)
        html = render(request, 'bilboard_artical.html', payload).content.decode('utf-8')
        response.content = html
        return response

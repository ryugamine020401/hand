"""
引用的順序 原本的套件、django的套件、本地內的引用
"""
import datetime

from django.shortcuts import render, redirect
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from reg.forms import LoginForm, EmailCheckForm
from reg.models import UserIfm
from reg.views import decode_access_token
from ifm.models import UserDefIfm
from forum.forms import ForumForm, ResponseForm
from forum.models import Discuss, DiscussResponse

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
            return redirect('../reg/login')

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
# ------------------------- 登入驗證裝飾器 ------------------------------
def loging_check(func):
    """
    登入確認，如果沒有找到登入的COOKIES會自度跳轉到登入的頁面。
    """
    def wrapper(req, request, artical_id=None): # pylint: disable=unused-argument
        token = request.COOKIES.get('access_token')
        if not token:
            form = LoginForm()
            payload = {
                "form" : form,
                "msg" : "請先登入後再執行該操作。"
            }
            response = Response(status=status.HTTP_200_OK)
            html = render(request, 'login.html', payload).content.decode('utf-8')
            response.content = html
            return response
        else:
            valdation = decode_access_token(token)['val']
            if valdation:
                # 驗證成功，代表使用信箱已經驗證了
                print("valdation success.")
            else:
                # 驗證失敗，代表使用信箱沒有驗證
                print()
                form = EmailCheckForm()
                payload = {
                    "form" : form,
                }
                response = Response(status=status.HTTP_200_OK)
                html = render(request, 'valdation_email.html', payload).content.decode('utf-8')
                response.content = html
                return response

            result = func(req, request, artical_id)
        return result
    return wrapper
# ------------------------- 登入驗證裝飾器 ------------------------------

class ForumSendView(APIView):
    """
    有登入帳號就可以使用發布文章的功能。
    """
    @loging_check
    def get(self, request, artical_id=None): # pylint: disable=unused-argument
        """
        獲得發送的頁面。
        """
        form = ForumForm()
        payload = {
            "form" : form,
        }
        response = Response(status=status.HTTP_202_ACCEPTED)
        html = render(request, 'forumsend.html', payload).content.decode('utf-8')
        response.content = html
        return response
    @loging_check
    def post(self, request, artical_id=None): # pylint: disable=unused-argument
        """
        送出輸入的文字
        """
        instance = Discuss()
        token = request.COOKIES.get('access_token')
        user_id = decode_access_token(token)['id']
        user_instance = UserIfm.objects.get(id = user_id)
        instance.user = user_instance
        instance.content = request.data['content']
        instance.title = request.data['title']
        instance.upload_date = str(datetime.date.today())
        instance.save()

        return redirect('./main')

class ForumView(APIView):
    """
    所有人都可以閱讀布告欄
    """
    @loging_check
    def get(self, request, artical_id=None):    # pylint: disable=unused-argument
        """
        獲得發送的頁面。
        """
        instance = Discuss.objects.all()
        payload = {
            "instance" : instance,
        }
        response = Response(status=status.HTTP_202_ACCEPTED)
        html = render(request, 'forum.html', payload).content.decode('utf-8')
        response.content = html
        return response

class ForumArticalView(APIView):
    """
    有登入可以使用查看所有討論的功能。
    """
    @loging_check
    def get(self, request, artical_id):
        """
        獲得發送的頁面。
        """
        instance = Discuss.objects.get(id=artical_id)
        author_headimg = UserDefIfm.objects.get(user_id = instance.user.id).headimg
        response = DiscussResponse.objects.filter(dis_id=artical_id)
        forms = ResponseForm()
        response_instance = []
        for res in response:
            # print(res.user_id)
            try:
                headimg = UserDefIfm.objects.get(user_id = res.user_id).headimg.url
                username = res.user_id.username
            except UserDefIfm.DoesNotExist as error_msg:    # pylint: disable=E1101
                print(error_msg)
                headimg = UserDefIfm.objects.get(user_id = 80928899).headimg.url
                username = "已刪除帳號"
            response_detial = {                     # 因為這邊的user_id也是FK 所以直接丟instance也沒關係
                'headimg' : headimg,  
                'response' : res.response,     
                'username' : username
            }
            response_instance.append(response_detial)
            # print(response_instance)
        # response_ifm = {
        #     "headimg" : ,
        #     "username" : ,
        # }
        payload = {
            "instance" : instance,
            "announcer" : instance.user.username,
            "headimg" : str(author_headimg.url),
            "response" : response_instance,
            "forms" : forms
        }
        response = Response(status=status.HTTP_200_OK)
        html = render(request, 'forum_artical.html', payload).content.decode('utf-8')
        response.content = html
        return response
    @loging_check
    def post(self, request, artical_id):
        """
        使用者回覆留言a
        """
        token = request.COOKIES.get('access_token')
        payload = decode_access_token(token=token)
        print(request, artical_id, 'addr', request.META['REMOTE_ADDR'])
        instance = DiscussResponse()
        user_instance = UserIfm.objects.get(id = payload['id'])
        discuss_instance = Discuss.objects.get(id = artical_id)

        instance.user_id = user_instance
        instance.response = request.data['response']
        instance.dis_id = discuss_instance
        instance.upload_date = str(datetime.date.today())
        instance.save()
        return redirect('./')

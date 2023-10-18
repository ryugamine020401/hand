"""
用來處理json的
"""
import json

import rest_framework
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed
from django.shortcuts import render

from channels.generic.websocket import WebsocketConsumer
from reg.forms import LoginForm, EmailCheckForm
from reg.models import UserIfm
from reg.views import decode_access_token
from ifm.models import UserDefIfm


from asgiref.sync import async_to_sync
# ------------------------- 登入驗證裝飾器 ------------------------------
def loging_check(func):
    """
    登入確認，如果沒有找到登入的COOKIES會自度跳轉到登入的頁面。
    """
    def wrapper(request):
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
                form = EmailCheckForm()
                payload = {
                    "form" : form,
                }
                response = Response(status=status.HTTP_200_OK)
                html = render(request, 'valdation_email.html', payload).content.decode('utf-8')
                response.content = html
                return response

            result = func(request)
        return result
    return wrapper
# ------------------------- 登入驗證裝飾器 ------------------------------
class ChatConsumer(WebsocketConsumer):
    """
    線上聊天室的comsumer
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.room_group_name = 'test'

    def connect(self):
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        self.accept()
        # self.send(text_data=json.dumps({
        #     'type':'connection_established',
        #     'message':'You are now connected!'
        # }))

    def receive(self, text_data=None, bytes_data=None):
        """
        使用者送出訊息。
        """
        text_data_json = json.loads(text_data)
        print(str(text_data_json['Authorization']).split()[1])
        token = str(text_data_json['Authorization']).split()[1]

        try:
            if token != b'null':
                print('有access token')
                user_id = decode_access_token(token)['id']
            username = UserIfm.objects.get(id=user_id).username
            headimg = UserDefIfm.objects.get(user_id=user_id).headimg
        except UserDefIfm.DoesNotExist as error_msg:    # pylint: disable=E1101
            print(error_msg, "1")
            username = "匿名"
            headimg = UserDefIfm.objects.get(user_id=47743479).headimg
        except KeyError as error_msg:
            print(error_msg, "沒有登入。")
            username = "我沒有登入"
            headimg = UserDefIfm.objects.get(user_id=47743479).headimg
        except rest_framework.exceptions.AuthenticationFailed as error_msg:
            print(error_msg)
            username = "我沒有登入"
            headimg = UserDefIfm.objects.get(user_id=47743479).headimg

        message = text_data_json['message']
        print(text_data_json)
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type' : 'chat_message',
                'message' : f'{message}',
                'headimg' : str(headimg.url),
                'username' : username,
            }
        )

    def chat_message(self, event):
        """
        發送訊息到已經建立連接的聊天室內。
        """
        message = event['message']
        headimg = event['headimg']
        username = event['username']
        self.send(text_data=json.dumps({
            'type' : 'chat',
            'message' : message,
            'headimg' : headimg,
            'username' : username
        }))

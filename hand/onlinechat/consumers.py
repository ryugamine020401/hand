"""
用來處理json的
"""
import json

from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render

from channels.generic.websocket import WebsocketConsumer
from reg.forms import LoginForm, EmailCheckForm
from reg.models import UserIfm
from ifm.models import UserDefIfm
from reg.views import decode_access_token
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
                print()
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
    
    def connect(self):
        self.room_group_name = 'test'
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        self.accept()
        # self.send(text_data=json.dumps({
        #     'type':'connection_established',
        #     'message':'You are now connected!'
        # }))
    
    def receive(self, text_data):
        # print(self.scope['cookies']['access_token'])
        try:
            token = self.scope['cookies']['access_token']
            user_id = decode_access_token(token)['id']
            username = UserIfm.objects.get(id=user_id).username
        except:
            username = "匿名"
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type' : 'chat_message',
                'message' : f'{username} : {message}'
            }
        )
        # print('Message', message)
        # self.send(text_data=json.dumps({
        #     'type':'chat',
        #     'message': message
        # }))
        
    def chat_message(self, event):
        message = event['message']
        self.send(text_data=json.dumps({
            'type' : 'chat',
            'message' : message
        }))

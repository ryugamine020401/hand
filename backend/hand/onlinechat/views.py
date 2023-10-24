"""
用來處理使用者引入字卡的時間
"""
# import datetime
# import numpy as np
# import mediapipe as mp
# import cv2

from django.shortcuts import render
from django.http import JsonResponse
# from rest_framework.authentication import get_authorization_header
from rest_framework.views import APIView
from rest_framework import status


from reg.views import decode_access_token
# from reg.models import UserIfm
from onlinechat.models import OlineChatroom
from reg.forms import LoginForm, EmailCheckForm

# -------------- 聊天室 ---------------
def lobby(request):
    return render(request, 'lobby.html', {})
# -------------- 聊天室 ---------------

# -------------- 聊天室獲取前幾筆聊天紀錄 ---------------
class GetLeastChatAPIView(APIView):
    def get(self, request):

        last_record = OlineChatroom.objects.order_by('-id').last()
        records = OlineChatroom.objects.order_by('id').reverse()[:5]
        print(records)
        messagelist = []
        for i in records[::-1]:
            data = {
                'message' : i.message,
                'headimg' : f'/getmedia/{i.message_img}',
                'username' : i.username,
            }
            messagelist.append(data)

        data = {
            'message':'成功獲得資料。',
            'content':messagelist
        }
        response = JsonResponse(data, status=status.HTTP_200_OK)
        return response
# -------------- 聊天室獲取前幾筆聊天紀錄 ---------------
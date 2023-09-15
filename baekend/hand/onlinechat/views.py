"""
用來處理使用者引入字卡的時間
"""
# import datetime
# import numpy as np
# import mediapipe as mp
# import cv2

from django.shortcuts import render

from rest_framework.response import Response
# from rest_framework.authentication import get_authorization_header
from rest_framework.views import APIView
from rest_framework import status


from reg.views import decode_access_token
# from reg.models import UserIfm
from reg.forms import LoginForm, EmailCheckForm
# from ifm.models import UseWordCard
# from study.models import TeachWordCard, TeachType
# from study.forms import UploadEnglishForm, UploadTeachTypeForm
# from study.serializers import UseWordCardSerializer
# from hand.settings import ROOT_EMAIL

# ------------------------- 登入驗證裝飾器 ------------------------------
def loging_check(func):
    """
    登入確認，如果沒有找到登入的COOKIES會自度跳轉到登入的頁面。
    """
    def wrapper(req, request):
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

            result = func(req, request)
        return result
    return wrapper
# ------------------------- 登入驗證裝飾器 ------------------------------

# -------------- 聊天室 ---------------
def lobby(request):
    return render(request, 'lobby.html', {})


# -------------- 聊天室 ---------------


import jwt

# import rest_framework.exceptions
# from django.http.response import HttpResponse
"""
用來處理送到前端的資料
"""
from django.shortcuts import render
# from django.core.mail import EmailMessage
# from django.conf import settings
# from django.template.loader import render_to_string


from rest_framework.response import Response
from rest_framework.authentication import get_authorization_header
from rest_framework.views import APIView
# from rest_framework import status

from reg.views import decode_access_token
# from reg.form import RegisterForm, LoginForm
from reg.serializers import RegisterSerializer
from reg.models import UserIfm

from ifm.serializers import UserDefIfmSerializer
from ifm.models import UserDefIfm
# from hand.settings import SECRET_KEY
# ------------------------------登入後的功能------------------------------
class IfmView(APIView):
    """
    使用者查看、修改自己個人資訊
    """
    def get(self, request):
        """
        前端打get需要查看個人資訊
        """
        # auth = get_authorization_header(request).split()
        # print(auth)

        # if (len(auth) == 2 and auth):
        #     token = auth[1].decode('utf-8')
        #     payload = decode_access_token(token=token)
        #     # user_email = payload['email']
        #     user_id = payload['id']
        # else:
        #     return Response({"msg":"no header."})
        token = request.COOKIES.get('access_token')
        payload = decode_access_token(token=token)
        user_id = payload['id']
        response = Response()

        response.data = {
            "email" : UserIfm.objects.get(id=user_id).email,
            "describe" : UserDefIfm.objects.get(user_id=user_id).describe,
            "username" : UserIfm.objects.get(id=user_id).username,
            "headimage" : UserDefIfm.objects.get(user_id=user_id).headimg,
        }
        payload = {
            "email" : UserIfm.objects.get(id=user_id).email,
            "describe" : UserDefIfm.objects.get(user_id=user_id).describe,
            "username" : UserIfm.objects.get(id=user_id).username,
            "headimage" : UserDefIfm.objects.get(user_id=user_id),
        }
        html = render(request, 'getinformation.html', payload).content.decode('utf-8')
        response.content = html
        return response

    def post(self, request):
        """
        修改使用者的資訊，會獲得
        UserDefIfm  頭像、個人簡介
        UserIfm     使用者名稱、電子郵件、出生日期
        所以需要透過兩個
        """
        auth = get_authorization_header(request).split()
        print(auth)

        if (len(auth) == 2 and auth):
            token = auth[1].decode('utf-8')
            payload = decode_access_token(token=token)
            # user_email = payload['email']
            user_id = payload['id']
        else:
            return Response({"msg":"Mo Access token."})

        ser1 = {
            'headimg' : request.data["headimg"],
            'describe' : request.data["describe"],
            'user_id' : user_id,      # 為了讓序列器is_valid所做的調整，不會更新db的資料
            'score' : 100.0,    # 為了讓序列器is_valid所做的調整，不會更新db的資料
        }

        ser2 = {
            'username' : request.data['username'],
            'email' : request.data['email'],
            'birthday' : request.data['birthday'],
            'password' : "n",
            'validation_num' : 0,
            'id' : user_id,
        }
        change_userdefifm = UserDefIfmSerializer(data=ser1)
        change_userifm = RegisterSerializer(data=ser2)

        if (change_userdefifm.is_valid() and change_userifm.is_valid()):
            change_userdefifm.update(UserDefIfm.objects.get(user_id=user_id), ser1)
            change_userifm.update1(UserIfm.objects.get(id=user_id), ser2)
        else:
            print(change_userdefifm.error_messages, change_userifm.error_messages)
        responese = Response()
        payload = {
            "msg" : "成功修改",
            "使用者id" : user_id,
            "狀態" : "返回ya面"
        }
        responese.data = payload
        return responese

    # def get(self, request):
    #     token = request.COOKIES.get('jwt')

    #     if (not token):
    #         return Response({"ERROR":"UNFIND COOKIE, REJECT."})
    #     # payload = jwt.decode(token, 'secret', algorithms=['HS256'])
    #     try:
    #         payload_access = jwt.decode(token, 'secret_token', algorithms="HS256")
    #     except jwt.ExpiredSignatureError:
    #         return Response({"ERROR":"TOKEN SIGNATURE ERROR qq, REJECT."})
            # sql= f'SELECT * FROM `reg_userifm` WHERE (`Email`="{payload["email"]}");'
    #     # user = UserIFM.objects.raw(sql)

    #     # 用.filter會找出一個list，裡面有包含email的所有行，加了first後又
    #     # 因為Email是Primarykey，因此只會是None或一個UserIFM的實例。
    #     user = UserIFM.objects.filter(Email=payload_access['email']).first()
    #     serializer = UserRegisterSerializer(user)

    #     # 沒有first後因為會返還一個list，但UserRegisterSerializer內要放的是一個實例
    #     # 而返還的list是由很多實例組成，且因為Email是Primarykey，因此只要user[0]就可以了。
    #     user = UserIFM.objects.filter(Email=payload_access['email'])
    #     serializer = UserRegisterSerializer(user[0])
    #     return Response(serializer.data)

# ------------------------------登入後的功能------------------------------

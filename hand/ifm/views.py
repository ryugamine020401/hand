# import rest_framework.exceptions
# from django.http.response import HttpResponse
# from django.shortcuts import render
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
from ifm.serializers import UserDefIfmSerializer
from reg.models import UserIfm
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
        auth = get_authorization_header(request).split()
        print(auth)

        if (len(auth) == 2 and auth):
            token = auth[1].decode('utf-8')
            user_email = decode_access_token(token=token)
        else:
            return Response({"msg":"Permission Denine."})
        db_userifm = UserIfm.objects.filter(Email=user_email).first()
        user_id = RegisterSerializer(db_userifm).data.get('id')
        db_userdefifm = UserIfm.objects.filter(id=user_id).first()
        response = Response()

        response.data = {
            "email":UserDefIfmSerializer(db_userdefifm).data.get('headimg'),
            "describe":UserDefIfmSerializer(db_userdefifm).data.get('describe'),
            "使用者名稱":RegisterSerializer(db_userifm).data.get('Username'),

        }
        return response
    
    def post(self, request):
        """
        修改使用者的資訊，會獲得
        UserDefIfm  頭像、個人簡介
        UserIfm     使用者名稱、電子郵件、出生日期
        所以需要透過兩個
        """
        ser1 = {
            'headimg' : request.data["headimg"],
            'describe' : request.data["describe"],
        }

        ser2 = {
            'Username' : request.data['Username'],
            'Email' : request.data['Email'],
            'Birthday' : request.data['Birthday']
        }
        change_userifm = RegisterSerializer(ser1)
        change_userdefifm = UserDefIfmSerializer(ser2)

        

        pass

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

# import rest_framework.exceptions
# from django.http.response import HttpResponse
"""
用來處理送到前端的資料
"""
from django.shortcuts import render, redirect
# from django.core.mail import EmailMessage
# from django.conf import settings
# from django.template.loader import render_to_string


from rest_framework.response import Response
from rest_framework.authentication import get_authorization_header
from rest_framework.views import APIView
from rest_framework import status

from reg.views import decode_access_token
# from reg.form import RegisterForm, LoginForm
from reg.serializers import RegisterSerializer
from reg.models import UserIfm
from ifm.serializers import UserDefIfmSerializer
from ifm.models import UserDefIfm, UseWordCard
from ifm.forms import ReProfileForm

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
            payload = decode_access_token(token=token)
            # user_email = payload['email']
            user_id = payload['id']
        else:
            # return Response({"msg":"no header."})
            print("msg :", "no header.")
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

    # def post(self, request):
    #     """
    #     測試用的 v1.1版本後改變URL了
    #     修改使用者的資訊，會獲得
    #     UserDefIfm  頭像、個人簡介
    #     UserIfm     使用者名稱、電子郵件、出生日期
    #     所以需要透過兩個
    #     """
    #     auth = get_authorization_header(request).split()
    #     print(auth)

    #     if (len(auth) == 2 and auth):
    #         token = auth[1].decode('utf-8')
    #         payload = decode_access_token(token=token)
    #         # user_email = payload['email']
    #         user_id = payload['id']
    #     else:
    #         return Response({"msg":"Mo Access token."})

    #     ser1 = {
    #         'headimg' : request.data["headimg"],
    #         'describe' : request.data["describe"],
    #         'user_id' : user_id,      # 為了讓序列器is_valid所做的調整，不會更新db的資料
    #         'score' : 100.0,    # 為了讓序列器is_valid所做的調整，不會更新db的資料
    #     }

    #     ser2 = {
    #         'username' : request.data['username'],
    #         'email' : request.data['email'],
    #         'birthday' : request.data['birthday'],
    #         'password' : "n",
    #         'validation_num' : 0,
    #         'id' : user_id,
    #     }
    #     change_userdefifm = UserDefIfmSerializer(data=ser1)
    #     change_userifm = RegisterSerializer(data=ser2)

    #     if (change_userdefifm.is_valid() and change_userifm.is_valid()):
    #         change_userdefifm.update(UserDefIfm.objects.get(user_id=user_id), ser1)
    #         change_userifm.update1(UserIfm.objects.get(id=user_id), ser2)
    #     else:
    #         print(change_userdefifm.error_messages, change_userifm.error_messages)
    #     responese = Response()
    #     payload = {
    #         "msg" : "成功修改",
    #         "使用者id" : user_id,
    #         "狀態" : "返回ya面"
    #     }
    #     responese.data = payload
    #     return responese

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

# --------------------------------修改頁面--------------------------------
class ResetprofileView(APIView):
    """
    使用者的修改個人資訊頁面
    """
    def get(self, request):
        """
        獲得修改的頁面
        """
        token = request.COOKIES.get('access_token')
        if token:
            decode_access_token(token=token)
        else :
            return Response("NO TOKEN")
        form = ReProfileForm()
        context = {
            'form' : form,
        }
        response  = Response(status=status.HTTP_202_ACCEPTED)
        html =  render(request, './remeishi.html', context=context)
        response.content = html
        return response

    def post(self, request):
        """
        送出修改後的資料
        """
        token = request.COOKIES.get('access_token')
        if token:
            payload = decode_access_token(token=token)
            user_id = payload['id']
        else:
            return Response("NO TOKEN")
        ser1 = {
            "headimg" : request.data["headimg"],
            "describe" : request.data["describe"],
            "user_id" : user_id,      # 為了讓序列器is_valid所做的調整，不會更新db的資料
            "score" : 100.0,    # 為了讓序列器is_valid所做的調整，不會更新db的資料
        }
        ser2 = {
            "username" : request.data['username'],
            "email" : request.data['email'],
            "birthday" : request.data['birthday'],
            "password" : "nochange",
            "validation_num" : 0,
            "id" : user_id,
        }
        # print(ser1)
        # print(ser2)
        change_userdefifm = UserDefIfmSerializer(data=ser1)
        change_userifm = RegisterSerializer(data=ser2)

        if (change_userdefifm.is_valid() and change_userifm.is_valid()):
            change_userdefifm.update(UserDefIfm.objects.get(user_id=user_id), ser1)
            change_userifm.update1(UserIfm.objects.get(id=user_id), ser2)
        else:
            change_userdefifm.is_valid()
            change_userifm.is_valid()
            print(change_userdefifm.errors,'\n', change_userifm.errors)
        # response = Response()
        # html = render(request, './getinformation', context={"msg" : "update successful."})
        return redirect('./Meishi')

# --------------------------------修改頁面--------------------------------
# --------------------------------字卡頁面--------------------------------
class KadoView(APIView):
    """
    使用者個人字卡的頁面。
    """
    def get(self, request):
        """
        獲取使用者個人字卡
        """
        token = request.COOKIES.get('access_token')
        if token:
            user_id = decode_access_token(token)['id']
            print(user_id)
            # get預期是會拿回一個instance 但filter可以拿回多個
        # wordcard_db = UseWordCard.objects.get(user_id=user_id)
        wordcard_db = UseWordCard.objects.filter(user_id=user_id)
        context = {
            "allwordcard" : wordcard_db
        }
        response = Response(status=status.HTTP_202_ACCEPTED)
        html = render(request, './userwordcard.html', context=context).content.decode('utf-8')
        response.content = html
        return response
    def post(self, request):
        """
        新增字卡
        """
        token = request.COOKIES.get('access_token')
        if token:
            user_id = decode_access_token(token)['id']
        print(request.data)
        for word in request.data:
            # print(str(word).rsplit('_', maxsplit=1)[-1])
            key = str(word).rsplit('_', maxsplit=1)[-1]
        UseWordCard.objects.filter(user_id = user_id, word = key).delete()
        return redirect('./kado')
    def delete(self, request):
        """
        刪除字卡
        """
        print(request.data)
        return Response("delete")
# --------------------------------字卡頁面--------------------------------

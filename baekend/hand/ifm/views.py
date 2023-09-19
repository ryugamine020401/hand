"""
用來處理送到前端的資料
"""
from django.shortcuts import render, redirect
from django.http import JsonResponse

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
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
from reg.forms import EmailCheckForm, LoginForm
from ifm.serializers import UserDefIfmSerializer
from ifm.models import UserDefIfm, UseWordCard
from ifm.forms import ReProfileForm

from hand.settings import DOMAIN_NAME
# ------------------------- 登入驗證裝飾器 ------------------------------
def loging_check(func):
    """
    登入確認，如果沒有找到登入的COOKIES會自度跳轉到登入的頁面。
    """
    def wrapper(req, request):
        token = request.COOKIES.get('access_token')
        if not token:
            print("沒有token")
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
                print("valdation success.已驗證信箱的使用者操作。")
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
# ------------------------------------------------------------------- -React Test -------------------------------------------
class IfmViewTestReact(APIView):
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
        #     # return Response({"msg":"no header."})
        #     print("msg :", "no header.")
        # token = request.COOKIES.get('access_token')
        # payload = decode_access_token(token=token)
        # user_id = payload['id']

        payload = {
            "email" : 'asdasd@asdsa.dasdasd',
            "describe" : 'asdasda;sjmd;am;dsad;asmdas;djailkbdlaknbsdlkas',
            "username" : 'UserIfm.objects.get(id=user_id).username',
            "headimage" : UserDefIfm.objects.get(user_id=64316155).headimg.url,
            # "form" : form,
        }
        return JsonResponse(payload)
        
# ------------------------------------------------------------------- -React Test -------------------------------------------
# ------------------------------登入後的功能------------------------------
# --------------- 獲取個人資訊 ----------------
class UserInformationAPIViwe(APIView):
    """
    獲得使用者資料的API
    需要有jwt的驗證
    """
    def get(self, request):
        """
        前端進入個人資訊業面會自動打過來。
        """
        auth = get_authorization_header(request).split()
        print(auth)
        try:
            if auth[1] == b'null':
                print("header內沒有token(但有Authorization)", 'UserInformationAPIViwe')
                data = {
                    'message' : 'header內沒有token(但有Authorization).'
                }
                response = JsonResponse(data, status=status.HTTP_403_FORBIDDEN)
                return response
        except IndexError as error_msg:
            print(error_msg, 'UserInformationAPIViwe')
            data = {
                    'message' : '沒有Authorization.'
                }
            response = JsonResponse(data, status=status.HTTP_400_BAD_REQUEST)
            return response

        token = auth[1]
        token_payload = decode_access_token(token)
        instance = UserDefIfm.objects.get(user_id = token_payload['id'])
        headimageurl = f'http://127.0.0.1:8000/ifm{instance.headimg.url}'
        data = {
            'message': "成功獲得",
            "username" : UserIfm.objects.get(id = token_payload['id']).username,
            "headimageurl" : headimageurl,
            "describe" : instance.describe,
        }

        response = JsonResponse(data, status=status.HTTP_200_OK)
        return response

# --------------------------------修改頁面--------------------------------
class ResetprofileView(APIView):
    """
    使用者的修改個人資訊頁面
    """
    @swagger_auto_schema(
        operation_summary='獲得修改個人資訊的頁面',
    )
    @loging_check
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
    @swagger_auto_schema(
        operation_summary='修改個人資訊',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'headimg':openapi.Schema(
                    type=openapi.TYPE_FILE,
                    description='頭像'
                ),
                'describe':openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description='狀態描述'
                ),
                'username':openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description='暱稱'
                ),
                'email':openapi.Schema(
                    type=openapi.FORMAT_EMAIL,
                    description='電子郵件'
                ),
                'birthday':openapi.Schema(
                    type=openapi.FORMAT_DATE,
                    description='生日'
                ),
            }
        )
    )
    @loging_check
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
# -------------------------- 獲得使用者個人字卡API -----------------------
class UserWordCardAPIView(APIView):
    """
    使用者可以獲得自己的字卡。
    """
    def get(self, request):
        """
        使用者進入頁面後會自動打get獲得需要的資源
        需要身分驗證
        """
        auth = get_authorization_header(request).split()

        try:
            token = auth[1]
            if token == b'null':
                data = {
                    'message' : "沒有token",
                }
                response = JsonResponse(data, status=status.HTTP_403_FORBIDDEN)
                return response
        except IndexError as error_msg:
            print(error_msg, 'GETCardAPIView')
            data = {
                'message' : '沒有Authorization.',
            }
            response =JsonResponse(data, status=status.HTTP_400_BAD_REQUEST)
            return response

        token_payload = decode_access_token(token)
        user_id = token_payload['id']
        # get預期是會拿回一個instance 但filter可以拿回多個
        # wordcard_db = UseWordCard.objects.get(user_id=user_id)
        wordcard_db = UseWordCard.objects.filter(user_id=user_id)

        ## ###################### test ######################
        # wordcard_db = UseWordCard.objects.filter(user_id=80928899)
        ## ###################### test ######################
        card_url_list = []
        card_url_diec = {}
        for instance in wordcard_db:
            card_url_list.append(DOMAIN_NAME+'/study'+instance.img.url)
            key = instance.word
            value = DOMAIN_NAME+'/study'+instance.img.url
            card_url_diec[key] = value
        print(card_url_diec)
        print(card_url_list)
        data = {
            'message' : '成功獲取字卡',
            'image_url_array' : card_url_list,
            'image_url_json' : card_url_diec,
        }

        response = JsonResponse(data, status=status.HTTP_200_OK)
        return response

    def delete(self, request):
        """
        使用者刪除他自己的字卡。
        """
        auth = get_authorization_header(request).split()
        try:
            if auth[1] == b'null':
                data = {
                    'message' : '沒有TOKEN',
                }
                response = JsonResponse(data, status=status.HTTP_403_FORBIDDEN)
            print(request.data)

        except IndexError as error_msg:
            print(error_msg, 'UserWordCardAPIView')
            data = {
                'message':'沒有Authorization.'
            }
            response = JsonResponse(data, status=status.HTTP_400_BAD_REQUEST)
            return response
        token_payload = decode_access_token(auth[1])
        user_id = token_payload['id']
        # 選擇出符合使用者選項 與 該使用者的字卡刪除      body只有要刪除的單字
        
        UseWordCard.objects.filter(user_id=user_id, word=request.data).delete()
        data = {
            'message' : '成功刪除',
        }
        return JsonResponse(data, status=status.HTTP_200_OK)


# -------------------------- 獲得使用者個人字卡API -----------------------
# --------------------------------字卡頁面--------------------------------
class KadoView(APIView):
    """
    使用者個人字卡的頁面。
    """
    @swagger_auto_schema(
        operation_summary='獲取個人字卡',
    )

    def get(self, request):
        """
        獲取使用者個人字卡
        """

            # get預期是會拿回一個instance 但filter可以拿回多個
        # wordcard_db = UseWordCard.objects.get(user_id=user_id)
        wordcard_db = UseWordCard.objects.filter(user_id=80928899)
        card_img_list = []
        for instance in wordcard_db:
            print(instance.img.url)
            card_img_list.append(instance.img.url)
            print(card_img_list)
        context = {
            "allwordcard" : wordcard_db
        }
        print(card_img_list)
        response = Response(status=status.HTTP_202_ACCEPTED)
        html = render(request, './userwordcard.html', context=context).content.decode('utf-8')
        response.content = html
        return response
    @swagger_auto_schema(
        operation_summary='刪除個人字卡',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'word':openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description='字卡內容'
                )
            }
        )
    )
    def post(self, request):
        """
        刪除字卡
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
    # def delete(self, request):
    #     """
    #     刪除字卡
    #     """
    #     print(request.data)
    #     return Response("delete")
# --------------------------------字卡頁面--------------------------------

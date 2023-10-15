"""
引入datetime方便記錄時間
產生JWT，套件是PyJWT==2.6.0
"""
import datetime
from hashlib import sha512  # hash加密
import random
import jwt
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from django.http.response import JsonResponse
from django.shortcuts import render, redirect
from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string


from rest_framework.response import Response
from rest_framework.authentication import get_authorization_header
from rest_framework.views import APIView
from rest_framework import status
import rest_framework.exceptions

from reg.forms import DeleteForm
from reg.serializers import RegisterSerializer
from reg.serializers import RegisterValidationSerializer
from reg.models import UserIfm

from ifm.models import UserDefIfm
from ifm.serializers import UserDefIfmSerializer


from hand.settings import SECRET_KEY, JWT_ACCRSS_TOKEN_KEY, JWT_REFRESH_TOKEN_KEY
from hand.settings import ROOT_EMAIL

from hand.settings import NGINX_DOMAIN   # 用來生成訪問圖像的網址

# ------------------------- 登入驗證裝飾器(header) ------------------------------
def loging_check(func):
    """
    登入確認，如果沒有找到登入的COOKIES會自度跳轉到登入的頁面。
    """
    def wrapper(req, request):
        auth = get_authorization_header(request).split()
        # print(auth, type(auth[1]))
        try:
            if auth[1] == b'null':
                request.custom_data = {
                    'token' : False,
                    'redirect' : './login' 
                }
            else:
                # print("有token")
                token = decode_access_token(auth[1])
                print(token)
                request.custom_data = {
                    'token' : True,
                    'redirect' : '../uchi' 
                }
            result = func(req, request)
            return result
        except IndexError as error_msg:
            print('裝飾器 @ 發生 ',error_msg)
            data = {
                'message' : '沒有Authorization'
            }
            response = JsonResponse(data, status=status.HTTP_400_BAD_REQUEST)
            return response
    return wrapper
# ------------------------- 登入驗證裝飾器(header) ------------------------------

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

# ---------------------------- 登入狀態確認 -------------------
class LoginCheckAPIView(APIView):
    """
    登入狀態的認證api 每一頁登入時會再狀態列顯示是否登入
    """
    def post(self, request):
        """
        會在用戶切換頁面時自動發送post到這個api
        """
        auth = get_authorization_header(request).split()
        try:
            if auth[1] != b'null':
                token_payload = decode_access_token(auth[1])
                if UserIfm.objects.get(id=token_payload['id']):
                    # 登入狀態正常
                    instance = UserIfm.objects.get(id=token_payload['id'])
                    img_url = NGINX_DOMAIN+'/api/ifm'
                    try:
                        img_url += UserDefIfm.objects.get(user_id=token_payload['id']).headimg.url
                    except UserDefIfm.DoesNotExist as error:    # pylint: disable=E1101
                        print(error)
                        data = {
                            'message':'沒有驗證',
                        }
                        response = JsonResponse(data, status=status.HTTP_401_UNAUTHORIZED)
                        return response
                    data = {
                        'loginstatus' : True,
                        'buttom_word' : f' {instance.username} 您好',   # 登入後單純傳文字
                        'headimgurl' : img_url,
                    }
                    response =JsonResponse(data, status=status.HTTP_200_OK)
                    return response
                else:
                    # 沒有登入狀態
                    data = {
                        'loginstatus' : False,
                        'buttom_word' : '登入',
                        'message' : '找不到用戶註冊資源。',
                    }
                    response =JsonResponse(data, status=status.HTTP_404_NOT_FOUND)
                    return response
            else:
                # header有Authorization但沒有內容物
                data = {
                    'loginstatus': False,
                    'buttom_word' : '登入',      # buttom顯示的文字
                    'message' :'找不到token。'
                }
                response =JsonResponse(data, status=status.HTTP_403_FORBIDDEN)
                return response
        except IndexError as error_msg:
            data = {
                    'loginstatus': False,
                    'buttom_word' : '登入',      # buttom顯示的文字
                    'message' : '缺少Authorization',
            }
            response =JsonResponse(data, status=status.HTTP_400_BAD_REQUEST)
            print(error_msg)
            return response
# ---------------------------- 登入狀態確認 -------------------
# ---------------------------- 註冊 ----------------------------------------------
class RegisterView(APIView):
    """
    註冊的Views其中包含
    GET 獲得表單
    POST 註冊
    """
    @swagger_auto_schema(
        operation_summary='送出註冊的內容',
        # operation_description='我是說明',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'name': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description='User Name'
                ),
                'email': openapi.Schema(
                    type=openapi.FORMAT_EMAIL,
                    description='User Email'
                ),
                'password1': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description='User Password'
                ),
                'password2': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description='Check User Password'
                ),
                'birthday': openapi.Schema(
                    type=openapi.FORMAT_DATE,
                    description='User Birthday'
                ),
            }
        )
    )
    def post(self, request):
        """
        前端打POST過來輸入好準備註冊
        """
        print(request.META)
        print(request.data)
        try:
            # 只有在網站內post才會有_mutable的屬性，用POSTMAN無效。
            # pylint: disable=protected-access
            request.data._mutable=True
        except AttributeError as error_msg:
            print(error_msg)
        serializer = RegisterSerializer(data=request.data)
        req_email = request.data["email"]
        print(req_email)
        if UserIfm.objects.raw(f'SELECT * FROM `reg_userifm`WHERE(`email`="{req_email}");'):
            data = {
                'message' : '帳號已經存在'
            }
            return JsonResponse(data, status=status.HTTP_409_CONFLICT)
        while True:   # 生成一個8位不重複的id
            tmp = int("".join(random.choices("0123456789", k=8)))   # 生成一個8位的數字
            if UserIfm.objects.raw(f'SELECT * FROM `reg_userifm`WHERE(`id`="{tmp}");'):
                continue
            else:
                break
        request.data['id'] = tmp
        passward = request.data['password']+str(tmp)
        request.data['password'] = sha512(passward.encode('utf-8')).hexdigest()
        request.data['validation_num'] = "".join(random.choices("0123456789", k=6))
        if serializer.is_valid():
            serializer.save()
            # 拉出要比對的實例
            user = UserIfm.objects.raw(f'SELECT * FROM `reg_userifm`WHERE(`id`="{tmp}");')[0]
            payload = {
                'email' : user.email,
                'val1' : user.validation_num,   # 驗證6碼
                'val2' : user.validation,       # 狀態
                'exp' : datetime.datetime.utcnow() + datetime.timedelta(days=7),
                'iat' : datetime.datetime.utcnow(),
            }
            validaton_token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
            email_template = render_to_string(
                './signup_success_email.html',
                {
                    'username': request.data['username'],
                    'validation_num' : request.data['validation_num'],
                    'validaton_token': validaton_token,
                }
            )
            email = EmailMessage(
                '註冊成功通知信',  # 電子郵件標題
                email_template,  # 電子郵件內容
                settings.EMAIL_HOST_USER,  # 寄件者
                [request.data['email']]  # 收件者
            )
            email.content_subtype = "html"
            email.fail_silently = False
            try:
                email.send()
            except OSError as error_msg:
                print(error_msg)
            access_token = creat_access_token(UserIfm.objects.get(email = user.email))
            data = {
                'validaton_token' : validaton_token,
                'access_token' : access_token,
                'message' : '註冊成功，請進入信箱驗證。'
            }
            response = JsonResponse(data, status=status.HTTP_201_CREATED)
            return response
        data = {
            'message' : '輸入的格式不符合要求',
        }
        return JsonResponse(data, status=status.HTTP_400_BAD_REQUEST)

# ---------------------------- 註冊 ----------------------------------------------
# ---------------------------- 註冊驗證 ------------------------------------------
class RegisterValidationView(APIView):
    """
    處理使用者的各種驗證狀態。
    """
    @swagger_auto_schema(
        operation_summary='驗證使用者信箱',
    )
    def post(self, request):
        """
        當用戶註冊完成後使用得到驗證碼進行驗證所打的POST
        直接抓取cookie方便在註冊完成後直接點及連結進行驗證
        """
        print(request)
        auth = get_authorization_header(request).split()
        try:
            if auth[1] == b'null':
                data = {
                    'message' : '沒有token。'
                }
                response = JsonResponse(data, status=status.HTTP_401_UNAUTHORIZED)
                return response
        except IndexError as error_msg:
            print(error_msg)
            data = {
                'message' : '沒有header。'
            }
            response = JsonResponse(data, status=status.HTTP_401_UNAUTHORIZED)
            return response
        token = auth[1]
        try:
            payload_validation = jwt.decode(token, SECRET_KEY, algorithms="HS256")
        except jwt.ExpiredSignatureError:
            return Response({"ERROR":"TOKEN SIGNATURE ERROR, REJECT."})

        request.data['email'] = payload_validation['email']
        serializer = RegisterValidationSerializer(data=request.data)


        try:
            sql = f'SELECT * FROM `reg_userifm` WHERE(`email`="{payload_validation["email"]}");'
            db_val1 = UserIfm.objects.raw(sql)[0].validation_num
            db_email = UserIfm.objects.raw(sql)[0].email
            if(payload_validation['val1'] == db_val1 and payload_validation['email'] == db_email):
                request.data['validation_num'] = -1
                request.data['validation'] = True

                if serializer.is_valid():
                    payload = {
                        'validation': True,
                        'validation_num': -1
                    }
                    email = f'{payload_validation["email"]}' # 包在jwt中的email
                    serializer.update(UserIfm.objects.get(email = email), payload)
                    user_id = UserIfm.objects.get(email=request.data['email']).id
                    # 驗證成功後會生成使用者的預設個人資料
                    seri_data = {
                            'describe' : '預設值空白留言。',
                            'user_id' : user_id,    # 先把數字送進去，之後再序列器內調整
                            'score' : 100.0
                        }
                    serializer = UserDefIfmSerializer(data=seri_data)
                    if serializer.is_valid() :
                        user_instance = UserIfm.objects.get(id=user_id)
                        access_token = creat_access_token(user_instance)
                        data = {
                            'message' : '驗證成功',
                            'redirect' : '../uchi',
                            'access_token' : access_token,
                        }
                        response = JsonResponse(data, status=status.HTTP_201_CREATED)
                        serializer.save()
                    else:
                        print("驗證沒有過QQ", serializer.errors)
                    return response
                else:
                    return Response('error,  資料格式錯誤。')
            else:
                if payload_validation['email'] == db_email:
                    data = {
                            'message' : '已經驗證過了。',
                            'redirect' : '../uchi'
                        }
                    response = JsonResponse(data, status=status.HTTP_302_FOUND)
                    return response
                else:
                    data = {
                            'message' : 'Email 錯誤請回報BUG並附上您的Email。',
                        }
                    response = JsonResponse(data, status=status.HTTP_410_GONE)
                    return response
        except IndexError as error_msg:
            print(error_msg)
            data = {
                'message' : '帳號不存在',
            }
            response = JsonResponse(data, status=status.HTTP_404_NOT_FOUND)
            return response # 已經驗證過或沒有這筆資料導致 index out of range
# ---------------------------- 註冊驗證 ------------------------------------------
# ----------------------------- 登入 ---------------------------------------------
class LoginView(APIView):
    """
    使用者登入
    """
    @swagger_auto_schema(
        operation_summary='獲得登入頁面',
    )
    @loging_check
    def get(self, request):
        """
        前端打GET過來想要進入網站
        """
        print(request.custom_data)
        if request.custom_data['token']:
            # 已經登入了
            print(request.custom_data)
            data = {
                'message' : 'success',
                'redirect': request.custom_data['redirect']
            }
            return JsonResponse(data, status=status.HTTP_200_OK)
        else:
            # 未登入 或 登入過期
            data = {
                'message' : '未登入',
                'redirect': request.custom_data['redirect']
            }
            return JsonResponse(data, status=status.HTTP_401_UNAUTHORIZED)

    @swagger_auto_schema(
        operation_summary='送出登入的內容',
        # operation_description='我是說明',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'email': openapi.Schema(
                    type=openapi.FORMAT_EMAIL,
                    description='User Email'
                ),
                'password': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description='User Password'
                ),
            }
        )
    )
    def post(self, request):
        """
        使用者登入的post
        """
        # print(request.META)
        # request.data是一個字典，裡面有所有傳入的東西。
        # 所以可以透過request.data.get('Email')來取得細部。
        # print(request.data)
        email = request.data.get("email")
        password = request.data.get("password")
        # 一個實例
        # db_data = UserIfm.objects.raw(f'SELECT * FROM `reg_userifm` WHERE(`email`="{email}");')
        try:
            db_data = UserIfm.objects.get(email = email)
        except UserIfm.DoesNotExist as error_msg:   # pylint: disable=E1101
            print(error_msg)
            data = {
                'message' : "帳號不存在"
            }
            response = JsonResponse(data, status=401)
            return response
        if db_data :
            password += str(db_data.id)
            # print(password)
            if db_data.password == sha512(password.encode('UTF-8')).hexdigest() :
                # 如果帳號正確
                access_token = creat_access_token(db_data)
                refresh_token = creat_refresh_token(db_data)
                # print("沒有next參數。")
                resource = [
                    '佈告欄', 
                    '討論區',
                    '學習中心',
                    '線上聊天室',
                    '個人資訊',
                    ]
                data = {
                    'resource' : resource,
                    'access_token' : access_token,
                    'refresh_token' : refresh_token
                }

                response = JsonResponse(data, status=status.HTTP_200_OK)
                return response
            else:
                print("密碼錯誤")
                data = {
                    'message': '密碼錯誤',
                    }
                response = JsonResponse(data, status=401)
                return response
        else:
            data = {
                    'message': '帳號不存在',
                    }
            response = JsonResponse(data, status=401)
            return response
# ----------------------------- 登入 ---------------------------------------------
# ----------------------------- 登出 ---------------------------------------------
class LogoutAPIView(APIView):
    """
    用來登出的API
    """
    @swagger_auto_schema(
        operation_summary='登出',
    )
    def get(self, request):
        """
        使用者打POST刪除COOKIES
        """
        print("使用者登出", request.COOKIES.get('access_token'))
        response = Response(status=status.HTTP_200_OK)
        response.delete_cookie('access_token')
        response.delete_cookie('refresh_token')
        return response
# ----------------------------- 登出 ---------------------------------------------


# ---------------------------- 忘記密碼 ------------------------------------------
# --------------- 忘記密碼的email寄送api --------------- OK
class ForgetPasswordValNumResendAPIView(APIView):
    """
    重新寄送使用者忘記密碼時填寫的郵件
    必須是已經註冊過的。
    """
    @swagger_auto_schema(
        operation_summary='忘記密碼需要信箱驗證',
        # operation_description='我是說明',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'email': openapi.Schema(
                    type=openapi.FORMAT_EMAIL,
                    description='User Email'
                ),
            }
        )
    )
    def post(self, request):
        """
        POST使後端重新寄送驗證信.
        """
        email = request.data['email']
        try:
            instance = UserIfm.objects.get(email=email)
        except UserIfm.DoesNotExist as error_msg:   # pylint: disable=E1101
            print("使用者不存在", error_msg)
            data = {
                'message' : '使用者不存在'
            }
            response = JsonResponse(data, status=status.HTTP_404_NOT_FOUND)
            return response
        instance.validation = False
        instance.validation_num = "".join(random.choices("0123456789", k=6))
        instance.save()
        email_template = render_to_string(
            './forget_password_email.html',
            {'username': instance.username,
                'validation_num' : instance.validation_num}
        )
        email = EmailMessage(
            '重設密碼通知信',  # 電子郵件標題
            email_template,  # 電子郵件內容
            settings.EMAIL_HOST_USER,  # 寄件者
            [instance.email]  # 收件者
        )
        email.content_subtype = "html"
        email.fail_silently = False
        try:
            email.send()
        except OSError as error_msg:
            print(error_msg)
            data = {
                'message' : '郵件發送失敗，請回報。'
            }
            response = JsonResponse(data, status= status.HTTP_500_INTERNAL_SERVER_ERROR)
            return response
        data = {
            'message' : '郵件發送成功。'
        }
        response = JsonResponse(data, status=status.HTTP_200_OK)
        return response
# --------------- email重新寄送 ---------------
# ------------ 忘記密碼的驗證API --------------
class ValdataeAPIViwe(APIView):
    """
    到忘記密碼頁面獲得驗證碼後需要驗證是否正確
    的API
    """
    def post(self, request):
        """
        只允許前端伺服器POST到後端伺服器。
        """
        print(request.data)
        try:
            email = request.data['email']
        except KeyError as error_msg:
            print(error_msg, ValdataeAPIViwe)
            auth = get_authorization_header(request).split()
            try:
                token = auth[1]
                if auth[1] == b'null':
                    data ={
                        'message' : '不正確的token.'
                    }
                    response = JsonResponse(data, status=status.HTTP_401_UNAUTHORIZED)
                    return response
                else:
                    email = decode_access_token(token=token)['email']
            except IndexError as error_msg2:
                print(error_msg2, ValdataeAPIViwe)
                data ={
                    'message' : '沒有Header'
                }
                response = JsonResponse(data, status=status.HTTP_400_BAD_REQUEST)
                return response

        try:
            if email == "":
                data = {
                    'message': "請輸入電子郵件"
                }
                response = JsonResponse(data, status=status.HTTP_400_BAD_REQUEST)
                return response
            instance = UserIfm.objects.get(email=email)
        except UserIfm.DoesNotExist as error:    # pylint: disable=E1101
            print(error, 'ValdataeAPIViwe')
            data = {
                'message' : '沒有這個使用者',
            }
            response = JsonResponse(data, status=status.HTTP_404_NOT_FOUND)
            return response
        if instance.validation_num == int(request.data['validationNum']):
            data = {
                'message' : '驗證成功，跳轉至修改密碼的頁面。',
                'email' : email,
            }
            instance = UserIfm.objects.get(email=email)
            instance.validation_num = -1
            instance.validation = True
            instance.save()
            response = JsonResponse(data, status=status.HTTP_200_OK)
            # 驗證成功後不會產生相對應的userdefifm表格，所以要在這邊產生
            try:
                # 帳號已經存在，不需要增加欄位
                _ = UserDefIfm.objects.get(user_id=instance.id)    # 檢查是否存在實例
                return response
            except UserDefIfm.DoesNotExist as error: #pylint: disable=E1101
                # 帳號不存在所以要新增欄位。
                print(error, ValdataeAPIViwe)
                user_id = instance.id
                seri_data = {
                        'describe' : '預設值空白留言。',
                        'user_id' : user_id,    # 先把數字送進去，之後再序列器內調整
                        'score' : 100.0
                    }
                serializer = UserDefIfmSerializer(data=seri_data)
                if serializer.is_valid() :
                    serializer.save()
                else:
                    print("驗證沒有過QQ", serializer.errors)
                return response

        else :
            print(instance.validation_num, request.data['validationNum'])
            print(type(instance.validation_num), type(request.data['validationNum']))
            data = {
                'message' : '驗證失敗，請輸入正確的驗證碼。',
                'redirect' : './',
            }
            response = JsonResponse(data, status=status.HTTP_401_UNAUTHORIZED)
            return response
# ------------ 忘記密碼的驗證API --------------
# --------------- 修改密碼 --------------------
class ResetPasswordAPIView(APIView):
    """
    忘記密碼時送出的驗證碼
    接收該驗證碼並確認是否正確的API。
    """
    @swagger_auto_schema(
        operation_summary='忘記密碼的重設密碼',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'email': openapi.Schema(
                    type=openapi.FORMAT_EMAIL,
                    description='User Email'
                ),
                'password': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description='User Password'
                ),
            }
        )
    )
    def post(self, request):
        """
        使用者輸入密碼後POST儲存
        """
        email = request.data['email']
        password = request.data['password']
        instance = UserIfm.objects.get(email = email)
        password += str(instance.id)
        instance.password = sha512(password.encode('UTF-8')).hexdigest()
        instance.save()
        data = {
            'message':'密碼修改成功',
            'redirect':'./login'
        }
        response = JsonResponse(data, status=status.HTTP_200_OK)
        return response
# --------------- 修改密碼 --------------------
# ---------------------------- 忘記密碼 ------------------------------------------


# ---------------------------- 重設密碼 ------------------------------------------
class PasswordResetViews(APIView):
    """
    使用者已經登入後重設密碼的視圖
    """
    @swagger_auto_schema(
        operation_summary='重設密碼',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'email': openapi.Schema(
                    type=openapi.FORMAT_EMAIL,
                    description='User Email'
                ),
                'password_old': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description='Check User Password'
                ),
                'password_new': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description='New User Password'
                ),
            }
        )
    )
    def post(self, request):
        """
        使用者送出更新的密碼
        """
        auth = get_authorization_header(request).split()
        try:
            if auth[1] == b'null':
                data = {
                    'message' : "沒有token.",
                }
                response = JsonResponse(data, status=status.HTTP_403_FORBIDDEN)
                return response
        except IndexError as error_msg:
            print(error_msg, 'PasswordResetViews')
            data = {
                    'message' : "Header格式錯誤",
                }
            response = JsonResponse(data, status=status.HTTP_400_BAD_REQUEST)
            return response
        token_payload = decode_access_token(auth[1])
        email = token_payload['email']
        password_old = request.data['password_old']
        password_new = request.data['password_new']
        userifm_instance = UserIfm.objects.get(email = email)
        password_old += str(userifm_instance.id)
        if userifm_instance.password == sha512(password_old.encode('UTF-8')).hexdigest():
            print("密碼正確，更新密碼。")
            password_new += str(userifm_instance.id)
            userifm_instance.password = sha512(password_new.encode('UTF-8')).hexdigest()
            userifm_instance.save()
            data = {
                    'message' : "修改成功",
                }
            response = JsonResponse(data, status=status.HTTP_200_OK)
            return response
        else:
            data = {
                    'message' : "密碼錯誤",
                }
            response = JsonResponse(data, status=status.HTTP_401_UNAUTHORIZED)
            return response
# ---------------------------- 重設密碼 ------------------------------------------

# ------------------------- email重新寄送 ------------------------------
class EmailReSendView(APIView):
    """
    重新寄送註冊郵件
    """
    @swagger_auto_schema(
        operation_summary='重寄驗證碼至信箱',
    )
    def post(self, request):
        """
        POST使後端重新寄送驗證信，需要帶有access token.
        不需要額外參數
        """
        auth = get_authorization_header(request).split()
        try:
            if auth[1] == b'null':
                data = {
                    'message':'沒有token',
                    'redirect':'./login',
                }
                response = JsonResponse(data, status=status.HTTP_401_UNAUTHORIZED)
                print('沒有token', 'EmailReSendView')
                return response
        except IndexError as error_msg:
            print(error_msg)
            data = {
                'error' : error_msg,
                'message' : '沒有Authorization.'
            }
            response  = JsonResponse(data, status=status.HTTP_400_BAD_REQUEST)
            return response
        user_id = decode_access_token(token=auth[1])['id']
        try:
            instance = UserIfm.objects.get(id=user_id)
        except UserIfm.DoesNotExist as error_msg:   # pylint: disable=E1101
            print(error_msg, EmailReSendView)
            data = {
                'message' : '找無此使用者。'
            }
            response = JsonResponse(data, status=status.HTTP_404_NOT_FOUND)
            return response

        email_template = render_to_string(
            './signup_success_email.html',
            {'username': instance.username,
                'validation_num' : instance.validation_num}
        )
        email = EmailMessage(
            '註冊成功通知信',  # 電子郵件標題
            email_template,  # 電子郵件內容
            settings.EMAIL_HOST_USER,  # 寄件者
            [instance.email]  # 收件者
        )
        email.content_subtype = "html"
        email.fail_silently = False
        try:
            email.send()
        except OSError as error_msg:
            print(error_msg)
            data = {
                'error' : error_msg,
                'message' : '請回報BUG'
            }
            response = JsonResponse(data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            return response
        data = {
            'message' : '成功重新寄送郵件',
        }
        response = JsonResponse(data, status=status.HTTP_200_OK)
        print('message', '成功重新寄送郵件。', 'EmailReSendView')
        return response
# ------------------------- email重新寄送 ------------------------------


# ------------------------- 刪除使用者 ---------------------------------
class DeleteUserIfmView(APIView):
    """
    root刪除使用者的視圖
    """
    @swagger_auto_schema(
        operation_summary='刪除使用者',
    )
    @root_check
    def get(self, request):
        """
        獲得刪除的頁面，需要有root權限。
        """
        all_inatance = UserIfm.objects.all()
        response = Response(status=status.HTTP_202_ACCEPTED)
        form = DeleteForm()
        payload = {
            "form" : form,
            "user_instance" : all_inatance
        }
        html = render(request, 'delete_account.html', payload).content.decode('utf-8')
        response.content = html
        return response
    @swagger_auto_schema(
        operation_summary='root刪除使用者的功能',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'uesr_id': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description='User ID'
                ),
            }
        )
    )
    @root_check
    def post(self, request):
        """
        刪除選定的使用者，需要有root權限。
        透過按鈕可以刪除該使用者的帳號
        """
        print(request.data)
        for key in request.data:
            req_list = str(key).rsplit('_', 1)
        user_id = req_list[1]
        UserIfm.objects.get(id = user_id).delete()
        response = Response(status=status.HTTP_202_ACCEPTED)
        response.data = {
            "msg" : f'已刪除 {user_id} 。'
        }
        return redirect('/reg/deleteaccount')
# ------------------------- 刪除使用者 ---------------------------------
#------------------------- TOKEN create、decode func. ----------------------------
def creat_access_token(user):
    """
    建立access token
    """
    payload_access = {
        'email' : user.email,
        'username' : user.username,
        'val' : user.validation,
        'id' : user.id,
        'exp' : datetime.datetime.utcnow() + datetime.timedelta(hours=1),
        'iat' : datetime.datetime.utcnow(),
        'iss' : 'YMZK',
    }
    token_access = jwt.encode(payload_access, JWT_ACCRSS_TOKEN_KEY, algorithm="HS256")
    return token_access

def creat_refresh_token(user):
    """
    建立refresh token
    """
    payload_refresh = {
        'username' : user.username,
        'val_num' : user.validation_num,
        'val' : user.validation,
        'exp' : datetime.datetime.utcnow() + datetime.timedelta(days=7),
        'iat' : datetime.datetime.utcnow(),
    }

    token_refresh = jwt.encode(payload_refresh, JWT_REFRESH_TOKEN_KEY, algorithm="HS256")
    return token_refresh



def decode_access_token(token):
    """
    拆解access_token
    """
    try:
        payload = jwt.decode(token, JWT_ACCRSS_TOKEN_KEY, algorithms=['HS256'])
        return {'email' : payload['email'], 'id' : payload['id'], 'val' : payload['val']}
    except Exception as error_msg:
        print(error_msg)
        text = "Forbidden, Signature has expired. TOKEN過期或沒有。"
        raise rest_framework.exceptions.AuthenticationFailed(text)

def decode_refresh_token(token):
    """
    拆解refresh_token
    """
    try:
        payload = jwt.decode(token, JWT_REFRESH_TOKEN_KEY, algorithms=['HS256'])
        return payload['username']
    except Exception as error_msg:
        print(error_msg)
        raise rest_framework.exceptions.AuthenticationFailed("erroe,  fail token.")

#------------------------- TOKEN create、decode func. ----------------------------

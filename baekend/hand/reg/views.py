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

from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string


from rest_framework.response import Response
from rest_framework.authentication import get_authorization_header
from rest_framework.views import APIView
from rest_framework import status
import rest_framework.exceptions

from reg.forms import RegisterForm, LoginForm, ResetPasswordForm, EmailCheckForm, DeleteForm
from reg.forms import ForgetPasswordForm, ResetForgetPasswordForm
from reg.serializers import RegisterSerializer
from reg.serializers import RegisterValidationSerializer
from reg.models import UserIfm

from ifm.serializers import UserDefIfmSerializer


from hand.settings import SECRET_KEY, JWT_ACCRSS_TOKEN_KEY, JWT_REFRESH_TOKEN_KEY
from hand.settings import ROOT_EMAIL
# ------------------------- 登入驗證裝飾器 ------------------------------
def loging_check(func):
    """
    登入確認，如果沒有找到登入的COOKIES會自度跳轉到登入的頁面。
    """
    def wrapper(req, request):
        print(request.META)
        token = request.COOKIES.get('access_token')
        if not token:
            data = {
                'message' : '登入時效已過期，請重新登入。',
                'redriect' : '/login'
            }
            response = JsonResponse(data, status=status.HTTP_401_UNAUTHORIZED)
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

# ------------------------- 登入驗證裝飾器(header) ------------------------------
def loging_check2(func):
    """
    登入確認，如果沒有找到登入的COOKIES會自度跳轉到登入的頁面。
    """
    def wrapper(req, request):
        auth = get_authorization_header(request).split()
        # print(auth, type(auth[1]))

        if auth[1] == b'null':
            # return Response({"msg":"no header."})
            # print("msg :", "no token. @loging_check2")
            request.custom_data = {
                'token' : False,
                'redirect' : '/login' 
            }
        else:
            # print("有token")
            request.custom_data = {
                'token' : True,
                'redirect' : '/uchi' 
            }
        result = func(req, request)
        return result
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

# ------------------------- test ------------------------------
@loging_check
def index(request):
    """
    測試用的w
    """
    print(UserIfm.objects.get(id=6333890))
    print(request)
    return HttpResponse("My First Django APP Page")
# ------------------------- test ------------------------------

# ---------------------------- 註冊 ----------------------------------------------
class RegisterView(APIView):
    """
    註冊的Views其中包含
    GET 獲得表單
    POST 註冊
    """
    @swagger_auto_schema(
        operation_summary='獲得註冊頁面 已棄用。',
    )
    def get(self, request):
        """
        已棄用。
        前端打GET過來想要進入網站
        """
        form = RegisterForm()
        context = {
            'form' : form,
        }
        return render(request, './register.html', context=context)
        # self.template_name = './register.html'
        # form = UserRegisterSerializer(data=request.data)

        # return Response(form.data)
    @swagger_auto_schema(
        operation_summary='已棄用。 送出註冊的內容',
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
            # tmp = int(random.random()*10**8)
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
            email_template = render_to_string(
                './signup_success_email.html',
                {'username': request.data['username'],
                 'validation_num' : request.data['validation_num']}
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
            data = {
                'validaton_token' : validaton_token,
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
    def get(self, request):
        """
        當用戶註冊完成後得到驗證的網址所打的GET
        """
        respomse = Response(status.HTTP_200_OK)
        token = request.COOKIES.get('Validation_cookie')
        if not token:
            return Response({"ERROR":"UNFIND COOKIE, REJECT."})
        respomse.data = {
            'msg' : "123",
            'msg2' : "456",
            'msg3' : "789",
        }
        print(jwt.decode(token, SECRET_KEY, algorithms="HS256"))
        return render(request, 'check.html', context=respomse.data)
    @swagger_auto_schema(
        operation_summary='驗證使用者信箱',
    )
    def post(self, request):
        """
        當用戶註冊完成後使用得到驗證碼進行驗證所打的POST
        直接抓取cookie方便在註冊完成後直接點及連結進行驗證
        """
        try:
            # pylint: disable=protected-access
            request.data._mutable=True
        except ValueError as error_msg:
            print(error_msg)
        token = request.COOKIES.get('Validation_cookie')

        if not token:
            return Response({"ERROR":"UNFIND COOKIE, REJECT."})
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
                    response = Response()
                    response.data = {
                            "validation" : " Successful, delete the cookie."
                    }
                    response.delete_cookie('Validation_cookie')
                    user_id = UserIfm.objects.get(email=request.data['email']).id
                    # 驗證成功後會生成使用者的預設個人資料
                    seri_data = {
                            'describe' : '還沒有留言。',
                            'user_id' : user_id,    # 先把數字送進去，之後再序列器內調整
                            'score' : 100.0
                        }
                    serializer = UserDefIfmSerializer(data=seri_data)
                    if serializer.is_valid() :
                        serializer.save()
                    else:
                        print("驗證沒有過QQ", serializer.errors)
                    return response
                else:
                    return Response('error,  資料格式錯誤。')
            else:
                if payload_validation['email'] == db_email:
                    return Response("Validation Fail, cuz u maybe already valdition.")
                else:
                    return Response("Email Fail")
        except IndexError as error_msg:
            print(error_msg)
            return Response("NO ACCUNT")    # 已經驗證過或沒有這筆資料導致 index out of range
# ---------------------------- 註冊驗證 ------------------------------------------
# ----------------------------- 登入 ---------------------------------------------
class LoginView(APIView):
    """
    使用者登入
    """
    @swagger_auto_schema(
        operation_summary='獲得登入頁面',
    )
    @loging_check2
    def get(self, request):
        """
        前端打GET過來想要進入網站
        """
        print(request.custom_data)
        if request.custom_data['token']:
            # 已經登入了
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
        print(request.META)
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
                response = Response()
                next_url = request.GET.get('next')
                response.data = {
                    'Status' : "SUCCESSUFL LOGIN",    
                }
                payload = {
                    'accesstoken' : access_token,
                    'next_url' : next_url
                }
                #                   key=,            value=,
                response.set_cookie('access_token', access_token, httponly=True, max_age=3600)
                response.set_cookie('refresh_token', refresh_token, httponly=True, max_age=604800)
                html = render(request, 'login_successful.html', payload).content.decode('utf-8')
                # print('access_token : ', access_token, 'refresh_token : ', refresh_token)
                response.content = html

                if (next_url and next_url != '/reg/login'):
                    print('有next_url', next_url)
                    return response
                else:
                    # 如果沒有 next 參數，重定向到默認頁面
                    # 即從一般的登入介面
                    print("沒有next參數。")
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
                    return response   # 待修正
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
class ForgetPasswordView(APIView):
    """
    處理使用者忘記密碼時的操作。
    """
    @swagger_auto_schema(
        operation_summary='獲得忘記密碼頁面',
    )
    def get(self, request):
        """
        在登入時選擇忘記密碼所跳轉的頁面
        """
        form = ForgetPasswordForm()
        payload = {
            "form" : form,
        }
        response = Response(status=status.HTTP_200_OK)
        html = render(request, 'forget_password.html', payload).content.decode('utf-8')
        response.content = html
        return response
    @swagger_auto_schema(
        operation_summary='忘記密碼',
        # operation_description='我是說明',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'email': openapi.Schema(
                    type=openapi.FORMAT_EMAIL,
                    description='User Email'
                ),
                'valdation_num': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description='驗證碼'
                ),
            }
        )
    )
    def post(self, request):
        """
        驗證完成功後進入修改密碼
        """
        email = request.data['email']
        form = ResetForgetPasswordForm(initial={"email":email})
        payload = {
            "form" : form,
            "email" : email
        }
        instance = UserIfm.objects.get(email=email)
        instance.validation = True
        instance.validation_num = -1
        instance.save()
        response = Response(status=status.HTTP_200_OK)
        html = render(request, 'forget_password_reset.html', payload).content.decode('utf-8')
        response.content = html
        return response
# --------------- email重新寄送api ---------------
class ForgetPasswordValNumResendAPIView(APIView):
    """
    重新寄送使用者忘記密碼時註冊郵件
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
        POST使後端重新寄送驗證信，需要帶有access token.
        """
        email = request.data['email']
        try:
            instance = UserIfm.objects.get(email=email)
        except UserIfm.DoesNotExist as error_msg:   # pylint: disable=E1101
            print("使用者不存在", error_msg)
            return Response(status=status.HTTP_400_BAD_REQUEST)
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
        # response = HttpResponseRedirect('../forgetpassword')
        # return response
        form = ForgetPasswordForm(initial={"email":request.data['email']})
        payload = {
            "form" : form,
            "email" : email
        }
        response = Response(status=status.HTTP_200_OK)
        access_token = creat_access_token(instance)
        response.set_cookie(key='access_token', value=access_token, httponly=True, max_age=3600)
        html = render(request, 'forget_password.html', payload).content.decode('utf-8')
        response.content = html
        return response
# --------------- email重新寄送 ---------------
# --------------- 修改密碼 --------------------
class ResetPasswordAPIView(APIView):
    """
    忘記密碼驗證完後方可修改。
    """
    @swagger_auto_schema(
        operation_summary='忘記密碼的重設密碼',
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
        使用者輸入密碼後POST儲存
        """
        email = request.data['email']
        password = request.data['password1']
        instance = UserIfm.objects.get(email = email)
        password += str(instance.id)
        instance.password = sha512(password.encode('UTF-8')).hexdigest()
        instance.save()
        # print(password, instance)
        return Response(status=status.HTTP_202_ACCEPTED)
# --------------- 修改密碼 --------------------
# ---------------------------- 忘記密碼 ------------------------------------------


# ---------------------------- 重設密碼 ------------------------------------------
class PasswordResetViews(APIView):
    """
    使用者重設密碼的視圖
    """
    @swagger_auto_schema(
        operation_summary='重設密碼',
    )
    def get(self, request):
        """
        使用者得到重設密碼的頁面。
        """
        form = ResetPasswordForm()
        payload = {
            "form" : form
        }
        response = Response(status=status.HTTP_200_OK)
        html = render(request, 'reset_password.html', payload).content.decode('utf-8')
        response.content = html
        return response
    @swagger_auto_schema(
        operation_summary='重設密碼',
        # operation_description='我是說明',
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
        # print(request.data)
        email = request.data['email']
        password_old = request.data['password_old']
        password_new = request.data['password_new']
        # print(password_old, password_new, email)
        userifm_instance = UserIfm.objects.get(email = email)
        password_old += str(userifm_instance.id)
        if userifm_instance.password == sha512(password_old.encode('UTF-8')).hexdigest():
            print("密碼正確，更新密碼。")
            password_new += str(userifm_instance.id)
            userifm_instance.password = sha512(password_new.encode('UTF-8')).hexdigest()
            userifm_instance.save()
            # print("儲存")
        else:
            print("使用者密碼錯誤。")
            return Response("密碼錯誤")
        response = Response(status=status.HTTP_200_OK)
        return response
# ---------------------------- 重設密碼 ------------------------------------------

# ------------------------- email驗證 ------------------------------
class EmailValdationView(APIView):
    """
    可以拿到驗證信箱的畫面
    """
    @swagger_auto_schema(
        operation_summary='信箱驗證',
    )
    def get(self, request):
        """
        可以得到驗證的頁面
        """
        form = EmailCheckForm
        payload = {
            "form" : form
        }
        response = Response(status=status.HTTP_200_OK)
        html = render(request, 'valdation_email.html', payload).content.decode('utf-8')
        response.content = html
        return response
    @swagger_auto_schema(
        operation_summary='驗證信箱',
        # operation_description='我是說明',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'valdation_num': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description='User Email'
                ),
            }
        )
    )
    def post(self, request):
        """
        用來送出驗證碼
        """
        token = request.COOKIES.get('access_token')
        # print(token)
        if not token:
            print(request.data['validation_num'])
            return Response("沒有token。")
        else:
            payload = decode_access_token(token)
        email = payload['email']

        instance = UserIfm.objects.get(email = email)
        print(type(instance.validation_num), type(request.data["validation_num"]))
        if instance.validation_num == int(request.data["validation_num"]):
            instance.validation_num = -1
            instance.validation = True
            instance.save()
        else:
            print("驗證碼錯誤")
            return Response("驗證碼錯誤")
        print(request.data)
        token_access = creat_access_token(instance)
        token_refresh = creat_refresh_token(instance)
        response = Response()
        response.delete_cookie('refresh_token')
        response.delete_cookie('access_token')
        response.set_cookie(key='refresh_token', value=token_refresh, httponly=True) # max_age
        response.set_cookie(key='access_token', value=token_access, httponly=True, max_age=3600)
        response.data = {"msg" : "驗證成功請重新登入。"}
        seri_data = {
                'describe' : '還沒有留言。',
                'user_id' : instance.id,    # 先把數字送進去，之後再序列器內調整
                'score' : 100.0
            }
        serializer = UserDefIfmSerializer(data=seri_data)
        if serializer.is_valid() :
            serializer.save()
        else:
            print("驗證沒有過QQ", serializer.errors)
        return response
# ------------------------- email驗證 ------------------------------


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
        print(request.data)
        token = request.COOKIES.get('access_token')
        user_id = decode_access_token(token=token)['id']
        instance = UserIfm.objects.get(id=user_id)
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
        return redirect('../valemail')
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
        # operation_description='我是說明',
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
            # print(str(key).rsplit('_', 1)) ['instance_info', '52545386']
            req_list = str(key).rsplit('_', 1)
        user_id = req_list[1]
        UserIfm.objects.get(id = user_id).delete()
        response = Response(status=status.HTTP_202_ACCEPTED)
        response.data = {
            "msg" : f'已刪除 {user_id} 。'
        }
        # print("刪除了", user_id) 302
        return redirect('/reg/deleteaccount')
# ------------------------- 刪除使用者 ---------------------------------
# ------------------------- 主頁 ---------------------------------
class HomePageView(APIView):
    """
    使用者進入網站後的預設頁面
    """
    @swagger_auto_schema(
        operation_summary='主頁',
    )
    def get(self, request):
        """
        獲得該頁面的資訊
        """
        title_list = {
            'billboard':'佈告欄',
            'forum':'討論區',
            'study':'學習中心',
            'onlinechat':'線上聊天室',
            'ifm':'個人資訊'
        }
        payload = {
            'title' : title_list,
        }
        return render(request, 'homepage.html', payload)
    @swagger_auto_schema(
        operation_summary='點選網站的內容',
        # operation_description='我是說明',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'page_id': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description='page ID'
                ),
            }
        )
    )
    def post(self, request):
        """
        可以跳轉到該跳轉的地方。
        """
        # print(request.data)
        keys_list = list(request.data.keys())
        redirect_path = keys_list[-1]
        print(redirect_path)
        return redirect(f'/{redirect_path}')
# ------------------------- 主頁 ---------------------------------

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
        text = "Forbidden, Signature has expired. TOKEN過期了。"
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

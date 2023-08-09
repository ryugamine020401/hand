"""
引入datetime方便記錄時間
產生JWT，套件是PyJWT==2.6.0
"""
import datetime
from hashlib import sha512  # hash加密
import random
import jwt


import rest_framework.exceptions
from django.http.response import HttpResponse
from django.shortcuts import render
from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string


from rest_framework.response import Response
# from rest_framework.authentication import get_authorization_header
from rest_framework.views import APIView
from rest_framework import status

from reg.form import RegisterForm, LoginForm
from reg.serializers import RegisterSerializer
from reg.serializers import RegisterValidationSerializer
from reg.models import UserIfm

from ifm.serializers import UserDefIfmSerializer


from hand.settings import SECRET_KEY
# ---------------------------- 註冊 ----------------------------------------------
class RegisterView(APIView):
    """
    註冊的Views其中包含
    GET 獲得表單
    POST 註冊
    """
    def get(self, request):
        """
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
    def post(self, request):
        """
        前端打POST過來輸入好準備註冊
        """
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
            return Response("Create ACCUNT Fail Account exist.")
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
            token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")

            # 獲取模板渲染後的HTML結果
            success_msg = 'CREATE ACCUNT SUCCESSFUL, YOU NEED TO CHEACK THE EMAIL TO VALIDATION.'
            payload = {
                'msg': success_msg, 
                'email' : req_email
            }
            html = render(request, 'register_successful.html', payload).content.decode('utf-8')

            # 透過Response返回HTML結果和設定的Cookie
            response = Response(status=status.HTTP_201_CREATED)
            response.content = html
            response.set_cookie(key="Validation_cookie", value=token, httponly=True)
            return response
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# ---------------------------- 註冊 ----------------------------------------------

# ---------------------------- 註冊驗證 ------------------------------------------
class RegisterValidationView(APIView):
    """
    處理使用者的各種驗證狀態。
    """
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

    def post(self, request):
        """
        當用戶註冊完成後使用得到驗證碼進行驗證所打的POST
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
            return Response({"ERROR":"TOKEN SIGNATURE ERROR qq, REJECT."})

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
                    seri_data = {
                            'describe' : '還沒有。',
                            'user_id' : user_id,    # 這邊的序列器不同
                            'score' : 100.0
                        }
                    serializer = UserDefIfmSerializer(data=seri_data)
                    if serializer.is_valid() :
                        serializer.save()
                    else:
                        print("驗證沒有過QQ", serializer.errors)
                    return response
                else:
                    return Response('NONO, ERROR')
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
    def get(self, request):
        """
        前端打GET過來想要進入網站
        """
        form = LoginForm()
        context = {
            'form' : form,
        }
        return render(request, './login.html', context=context)

    def post(self, request):
        """
        使用者登入的post
        """
        # request.data是一個字典，裡面有所有傳入的東西。
        # 所以可以透過request.data.get('Email')來取得細部。
        email = request.data.get("email")
        password = request.data.get("password")
        # 一個實例
        db_data = UserIfm.objects.raw(f'SELECT * FROM `reg_userifm` WHERE(`email`="{email}");')
        if db_data :
            password += str(db_data[0].id)
            # print(password)
            if db_data[0].password == sha512(password.encode('UTF-8')).hexdigest() :
                # 如果帳號正確
                token_access = creat_access_token(db_data[0])
                token_refresh = creat_refresh_token(db_data[0])
                response = Response()
                response.set_cookie(key='refresh_token', value=token_refresh, httponly=True)
                response.data = {
                    'Status' : "SUCCESSUFL LOGIN",
                    'Access' : token_access,
                    'Refresh' :token_refresh,
                }
                payload = {
                    'accesstoken' : token_access
                }
                response.set_cookie(key='access_token', value=token_access, httponly=True)
                html = render(request, 'login_successful.html', payload).content.decode('utf-8')
                response.content = html
                return response
            else:
                return Response("Password WRONG")
        else:
            return Response("NO ACCUNT")
# ----------------------------- 登入 ---------------------------------------------

#------------------------- TOKEN create、decode func. ----------------------------
def creat_access_token(user):
    """
    建立access token
    """
    payload_access = {
        'email' : user.email,
        'username' : user.username,
        'Val' : user.validation,
        'id' : user.id,
        'exp' : datetime.datetime.utcnow() + datetime.timedelta(hours=1),
        'iat' : datetime.datetime.utcnow(),
        'iss' : 'YMZK',
    }
    token_access = jwt.encode(payload_access, 'secret_token', algorithm="HS256")
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

    token_refresh = jwt.encode(payload_refresh, 'refresh_secret', algorithm="HS256")
    return token_refresh



def decode_access_token(token):
    """
    拆解access_token
    """
    try:
        payload = jwt.decode(token, 'secret_token', algorithms=['HS256'])
        return {'email' : payload['email'], 'id' : payload['id']}
    except Exception as error_msg:
        print(error_msg)
        raise rest_framework.exceptions.AuthenticationFailed("ERROE, TOKEN FAIL.")

def decode_refresh_token(token):
    """
    拆解refresh_token
    """
    try:
        payload = jwt.decode(token, 'refresh_secret', algorithms=['HS256'])
        return payload['username']
    except Exception as error_msg:
        print(error_msg)
        raise rest_framework.exceptions.AuthenticationFailed("erroe,  fail token.")

#------------------------- TOKEN create、decode func. ----------------------------




def index(request):
    """
    測試用的
    """
    UserIfm.objects.get(id=31589525).delete()
    return HttpResponse("My First Django APP Page")

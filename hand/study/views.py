"""
用來處理使用者引入字卡的時間
"""
import datetime
import base64
import random
import numpy as np
import mediapipe as mp
import cv2

from django.shortcuts import render, redirect
from django.http import JsonResponse

from rest_framework.response import Response
# from rest_framework.authentication import get_authorization_header
from rest_framework.views import APIView
from rest_framework import status


from reg.views import decode_access_token
from reg.models import UserIfm
from reg.forms import LoginForm, EmailCheckForm
from ifm.models import UseWordCard
from study.models import TeachWordCard, TeachType
from study.forms import UploadEnglishForm, UploadTeachTypeForm
from study.serializers import UseWordCardSerializer
from hand.settings import ROOT_EMAIL
def root_check(func):
    """
    登入確認，如果沒有找到登入的COOKIES會自度跳轉到登入的頁面。
    """
    def wrapper(req, request):
        print("\n",request, req)
        token = request.COOKIES.get('access_token')

        if not token:
            return redirect('../reg/api/login')#

        user = decode_access_token(token)['id']
        instance = UserIfm.objects.get(email=ROOT_EMAIL)
        root_id = instance.id
        if user == root_id:
            result = func(req, request)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN, data = "權限不足")
        return result
    return wrapper

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

# ------------------------- test ------------------------------
def aaa(img):
    """
    老鐘寫的，可以用來辨識是否有手。
    """
    mp_hands = mp.solutions.hands                    # mediapipe 偵測手掌方法
    # img = cv2.imread('D:/work/aaa.jpg')
    with mp_hands.Hands(
        model_complexity=1,     # 複雜度越高越準確，但會增加延遲
        max_num_hands=1,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5) as hands:
        results = hands.process(img)  # 偵測手掌
        if results.multi_hand_landmarks:
            return True
        else:
            return False

class TestUploadImgView(APIView):
    """
    上傳圖片用的
    """

    def get(self, request):
        """
        獲得修改的頁面
        """
        form = UploadEnglishForm()
        context = {
            'form' : form,
        }
        response  = Response(status=status.HTTP_202_ACCEPTED)
        html =  render(request, './test.html', context=context)
        response.content = html
        return response

    def post(self, request):
        """
        送出修改後的資料
        """
        img = request.FILES['img']
        print(request.data)
        # print(img.read()) #獲得二進制資料
        # 將二進位資料轉換成NumPy陣列
        np_image = np.frombuffer(img.read(), np.uint8)
        print(np_image)
        # 使用OpenCV讀取圖片
        img = cv2.imdecode(np_image, cv2.IMREAD_COLOR)  # pylint: disable=E1101
        print(img)
        print(aaa(img=img))
        return Response({"successful"})

class UpLoadImgView(APIView):
    """
    測試test用的views
    """
    def get(self, request):
        """
        開相機跟傳輸資料基本上只有前端再處理。
        """
        return render(request, 'kamera.html', {})
    def post(self, request):
        """
        後端接收照片並處理後
        """
        encoded_image = request.data['image']
        # 從 Base64 編碼的字符串中解碼圖片數據
        decoded_image = base64.b64decode(encoded_image.split(',')[1])
        # 將二進制圖片數據轉換為 NumPy 數組
        image_array = np.frombuffer(decoded_image, dtype=np.uint8)
        image_array = cv2.imdecode(image_array, cv2.IMREAD_COLOR) # pylint: disable=E1101
        print(image_array.size)
        result = aaa(img=image_array)
        print(result)
        # path = '/home/ymzk/桌面/HAND/hand/study/TEST/img.png'
        # cv2.imwrite(path, image_array) # pylint: disable=E1101
        return JsonResponse({'message': 'Photo uploaded successfully'})
# ------------------------- test ------------------------------

# --------------------------------上傳教學圖片--------------------------------
class UploadStudyFileView(APIView):
    """
    上傳圖片用的
    """
    @root_check
    def get(self, request):
        """
        獲得修改的頁面
        """
        form = UploadEnglishForm()
        context = {
            'form' : form,
        }
        response  = Response(status=status.HTTP_202_ACCEPTED)
        html =  render(request, './uploadimage.html', context=context)
        response.content = html
        return response
    @root_check
    def post(self, request):
        """
        送出修改後的資料
        """
        des = request.data.getlist('describe')
        img = request.data.getlist('img')
        print(des)
        print(img)
        # for i in range(len(des)):
        #     print(type(i))
        #     database = TeachWordCard()
        #     database.img = img[i]
        #     database.describe = des[i]
        #     database.upload_date = '2023-08-11'
        #     database.save()
        #     print(database)
        for i, item in enumerate(img):
            database = TeachWordCard()
            database.img = img[i]
            database.describe = des[i]
            database.upload_date = '2023-08-11'
            database.save()
            print(database, f'已經儲存到第{i+1}筆資料。{item}')
        return Response({"successful"})

# ----------------------------上傳教學圖片--------------------------------

# ----------------------------上傳教學類別--------------------------------
class UploadTeachTypeView(APIView):
    """
    上傳圖片用的
    """
    @root_check
    def get(self, request):
        """
        獲得修改的頁面
        """
        form = UploadTeachTypeForm()
        context = {
            'form' : form,
        }
        response  = Response(status=status.HTTP_202_ACCEPTED)
        html =  render(request, './upload.html', context=context)
        response.content = html
        return response
    @root_check
    def post(self, request):
        """
        送出修改後的資料
        """
        des = request.data.getlist('type')
        print(des)
        # for i in range(len(des)):
        #     print(type(i))
        #     database = TeachType()
        #     database.type = des[i]
        for num, item in enumerate(des):
            database = TeachType()
            print(num)
            database.type = item
            database.save()
        return Response({"successful"})

# ----------------------------上傳教學類別--------------------------------

# ----------------------------學習中心------------------------------------
class TeachingCenterView(APIView):
    """
    讓使用者獲取目前擁有的教學資源    
    """
    def get(self, request):
        """
        讓使用者得到可以選擇的學習資源
        """
        tecahtype = TeachType.objects.all()
        print(tecahtype)
        response = Response(status=status.HTTP_200_OK)
        context = {
            "type" : tecahtype,
        }
        html = render(request, './home.html', context=context).content.decode('utf-8')
        response.content = html
        return response

# ----------------------------學習中心------------------------------------
# ------------------------學習中心_英文------------------------------------
class TeachingCenterEnglishView(APIView):
    """
    讓使用者獲取目前擁有的詳細教學資源    
    """
    def get(self, request):
        """
        讓使用者得到可以選擇的英文學習資源
        """
        english_alphabet = TeachWordCard.objects.all()
        response = Response(status=status.HTTP_200_OK)
        context = {
            "english_alphabet" : english_alphabet,
        }
        html = render(request, './english.html', context=context).content.decode('utf-8')
        response.content = html
        return response
    @loging_check
    def post(self, request):
        """
        加入使用者個人字卡
        """

        token = request.COOKIES.get('access_token')
        if token:
            user_id = decode_access_token(token)['id']
        else:
            return Response("NO TOKEN")
        now_time = datetime.datetime.now()
        for key in request.data:
            # print(str(key).rsplit('_', maxsplit=1)[-1])
            card_id = str(key).rsplit('_', maxsplit=1)[-1]
            # print(card_id, type(card_id), type(now_time.strftime("%Y-%m-%d")))
            # print(TeachWordCard.objects.get(id = int(card_id)).img)
        try:
            word = chr(int(card_id)+ 96)    # ASCII a是97 card_id是從1~26
            check_multiple = UseWordCard.objects.get(user_id = user_id, word = word)
            if check_multiple:
                return Response("字卡已經存在")
            print(check_multiple)

        # 查無此資料可以儲存，但會例外所以expect
        except UseWordCard.DoesNotExist as error: # pylint: disable=E1101
            print("目前無此資料，正常儲存。", error)

        # 已經存在的字卡不需要重新儲存
        except UseWordCard.MultipleObjectsReturned as error:    # pylint: disable=E1101
            print("不存", error)
            # 超過兩個以上的情況。
            return redirect('./english')

        ser = {
            "user_id" : user_id,
            "img" : TeachWordCard.objects.get(id = int(card_id)).img,
            "word" : word,    
            "upload_date" : now_time.strftime("%Y-%m-%d"),
        }
        serializer = UseWordCardSerializer(data=ser)

        if serializer.is_valid():
            print("success")
            serializer.save()
        else:
            print(serializer.errors)
        response = Response(status=status.HTTP_202_ACCEPTED)
        return response
# ------------------------學習中心_英文------------------------------------


# ------------------------測驗_1-------------------------------------------
# ------------------- 登入驗證裝飾器 ---------------------
def loging_check_test(func):
    """
    登入確認，如果沒有找到登入的COOKIES會自度跳轉到登入的頁面。
    """
    def wrapper(req, request, param1, param2):
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
                form = EmailCheckForm()
                payload = {
                    "form" : form,
                }
                response = Response(status=status.HTTP_200_OK)
                html = render(request, 'valdation_email.html', payload).content.decode('utf-8')
                response.content = html
                return response

            result = func(req, request, param1, param2)
        return result
    return wrapper
# ------------------- 登入驗證裝飾器 ---------------------

class TestOneViews(APIView):
    """
    測驗1 英文26字母手勢辨識
    """
    @loging_check_test
    def get(self, request, param1, param2):
        """
        獲得頁面。
        """
        random_int = random.randint(1, 26)
        alphabet = TeachWordCard.objects.get(id=random_int).describe
        response = Response(status=status.HTTP_202_ACCEPTED)
        payload = {
            "para1": param1,
            "para2": param2,
            "msg :" : 'test',
            "num" : param2+1,
            "mondai" : alphabet
        }
        html = render(request, 'test_one.html', payload).content.decode('utf-8')
        response.content = html
        return response
    def post(self, request, param1, param2):
        """
        使用者送出圖片。
        """
        # print(request.path, param1, param2)
        # print(param2+1)
        encoded_image = request.data['image']
        # 從 Base64 編碼的字符串中解碼圖片數據
        decoded_image = base64.b64decode(encoded_image.split(',')[1])
        # 將二進制圖片數據轉換為 NumPy 數組
        image_array = np.frombuffer(decoded_image, dtype=np.uint8)
        image_array = cv2.imdecode(image_array, cv2.IMREAD_COLOR) # pylint: disable=E1101
        print(image_array.size)
        result = aaa(img=image_array)
        print(result)
        return JsonResponse({'redirect_url' : f'../../{param1}/{param2+1}', 'detected':result})
# ------------------------測驗_1------------------------------------

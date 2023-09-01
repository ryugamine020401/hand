"""
用來處理使用者引入字卡的時間
"""
import os
import datetime
import base64
import random
import numpy as np
import mediapipe as mp
import cv2
from cvzone.HandTrackingModule import HandDetector
from keras.models import load_model


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
# from .hand.prediction import num2alphabet, predict
from hand.settings import MODEL_FILE_PATH
def root_check(func):
    """
    登入確認，如果沒有找到登入的COOKIES會自度跳轉到登入的頁面。
    """
    def wrapper(req, request):
        print("\n",request, req)
        token = request.COOKIES.get('access_token')

        if not token:
            form = LoginForm()
            payload = {
                "form" : form,
                "msg" : "請先登入後再執行該操作。"
            }
            response = Response(status=status.HTTP_202_ACCEPTED)
            html = render(request, 'login.html', payload).content.decode('utf-8')
            response.content = html
            return response
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
# ------------------------- 辨識 ------------------------------

model = load_model("study/signDot.h5")
def num2alphabet(text):
    """
    將預測結果轉為英文字母
    """
    alphabet = 'ABCDEFGHIKLMNOPQRSTUVWXY'
    return alphabet[text]

                # 正解
# BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# MODEL_FILE_PATH = os.path.join(BASE_DIR, 'static', 'models', 'signDot.h5')

def predict(img, correct):
    """
    預測結果
    """

    detector = HandDetector(detectionCon=0.5, maxHands=1)  # cvzone,用於抓出手部位置
    # model_file_path = os.path.join(os.path.dirname(__file__), 'static', 'models', 'signDot.h5')

    mp_hands = mp.solutions.hands  # mediapipe 偵測手掌方法
    hands_dot = mp_hands.Hands(
        model_complexity=1,  # 複雜度越高越準確，但會增加延遲
        max_num_hands=1,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5)

    hands = detector.findHands(img, draw=False)  # 使用cvzone抓出手部位置
    if hands:  # 若畫面中有手，並成功偵測到
        hand1 = hands[0]
        img_x, img_y, img_w, img_h = hand1['bbox']  # 抓出手部座標
        # print(x, y, w, h, sep=' ')
        if img_w > img_h:  # 擷取手部的影像，並且確保擷取結果為爭方形，且不超出原圖範圍
            img_y = int(img_y - (img_w - img_h) / 2)
            img_h = img_w
        else:
            img_x = int(img_x - (img_h - img_w) / 2)
            img_w = img_h
        img = img[img_y - 20:img_y + img_h + 20, img_x - 20:img_x + img_w + 20]
        if img_x - 20 > 0 and img_x + img_w + 20 < 765 and img_y - 20 > 0:
            rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # 轉RGB # pylint: disable=E1101
            rgb_img = cv2.resize(rgb_img, (128, 128))  # 調整圖片大小 # pylint: disable=E1101
            results = hands_dot.process(rgb_img)  # 偵測手部關節點座標
            finger_points = []  # 記錄手指節點座標的陣列

            if results.multi_hand_landmarks:  # 若成功抓到座標
                for hand_landmarks in results.multi_hand_landmarks:
                    for i in hand_landmarks.landmark:
                        # 將 21 個節點換算成座標，記錄到 finger_points
                        finger_points.append(i.x)
                        finger_points.append(i.y)
                finger_points = np.array(finger_points)  # 轉為numpy array
                finger_points = finger_points.reshape(1, 42)  # reshape
                # print(finger_points.shape)
                prediction = model.predict(finger_points, verbose=0)  # 輸出的是編碼
                index = np.argmax(prediction)  # 將編碼轉換後才是結果
                text = num2alphabet(index)
                # return round(prediction.max(), 3), text
                ans = {}
                alphabet = 'ABCDEFGHIKLMNOPQRSTUVWXY'
                count = 0
                for a in alphabet:
                    ans[a] = prediction[0][count]
                    count = count + 1
                response = {
                    'result': text,
                    'result_score': ans[text],
                    'correct_score': ans[correct]
                }
                return response
            else:
                # response = {
                #     'result': False,
                #     'result_score': ans[text],
                #     'correct_score': ans[correct],
                #     'msg' : 'mediapipe沒偵測到',
                #     'detected' : False
                # }
                print('mediapipe沒偵測到')
                return 'mediapipe沒偵測到'
        else:
            # response = {
            #         'result': False,
            #         'result_score': ans[text],
            #         'correct_score': ans[correct],
            #         'msg' : '手太靠近螢幕邊緣',
            #         'detected' : False
            #     }
            print('手太靠近螢幕邊緣')
            return '手太靠近螢幕邊緣'
    else:
        # response = {
        #             'result': False,
        #             'result_score': ans[text],
        #             'correct_score': ans[correct],
        #             'msg' : '沒手',
        #             'detected' : False
        #         }
        print('no hands')
        return 'no hands'

# ------------------------- 辨識 ------------------------------
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
        image_array = cv2.imdecode(np_image, cv2.IMREAD_COLOR) # pylint: disable=E1101
        image_array = cv2.cvtColor(image_array, cv2.COLOR_BGR2RGB) # pylint: disable=E1101
        print(image_array.size)
        result = aaa(img=image_array)
        print("結果一", result)
        result = predict(img=image_array, correct='c')
        print("結果二", result)
        # print(np_image)
        # # 使用OpenCV讀取圖片
        # img = cv2.imdecode(np_image, cv2.IMREAD_COLOR)  # pylint: disable=E1101
        # print(img)
        # print(aaa(img=img))
        return Response({"successful"})

class UpLoadImgView(APIView):
    """
    已棄用
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
        image_array = cv2.cvtColor(image_array, cv2.COLOR_BGR2RGB) # pylint: disable=E1101
        print(image_array.size)
        result = aaa(img=image_array)
        print("結果一", result)
        result = predict(img=image_array, correct='c')
        print("結果二", result)
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
        response = Response(status=status.HTTP_200_OK)
        tecahtype = {
            'english': '英文字母',
            'test/1/0' : '測驗1',
            'test/2/0' : '測驗2'
        }
        context = {
            "resourcetype" : tecahtype,
        }
        html = render(request, './home.html', context=context).content.decode('utf-8')
        response.content = html
        return response

    def post(self, request):
        """
        使用者點選後自動跳轉
        """
        keys_list = list(request.data.keys())
        redirect_path = keys_list[-1]
        # print(redirect_path)
        return redirect(f'./{redirect_path}')

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
                msg = 'UseWordCardExist'
                return redirect(f'./english?msg={msg}')
            print(check_multiple)

        # 查無此資料可以儲存，但會例外所以expect
        except UseWordCard.DoesNotExist as error: # pylint: disable=E1101
            print("目前無此資料，正常儲存。", error)

        # 已經存在的字卡不需要重新儲存
        except UseWordCard.MultipleObjectsReturned as error:    # pylint: disable=E1101
            print("不存", error)
            # 超過兩個以上的情況。
            msg = 'UseWordCardExist'
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
        # response = Response(status=status.HTTP_202_ACCEPTED)
        return redirect('../ifm/kado')
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

# ------------------------測驗_1------------------------------------
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
        alphabet = chr(TeachWordCard.objects.get(id=random_int).id)
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
        image_array = cv2.cvtColor(image_array, cv2.COLOR_BGR2RGB) # pylint: disable=E1101
        # image_array = cv2.resize(image_array, (128, 128)) # pylint: disable=E1101
        print(type(image_array))
        cv2.imwrite("./img.png", image_array) # pylint: disable=E1101
        print("儲存")
        print(image_array.size)
        result = aaa(img=image_array)
        result = predict(img = image_array, correct = 'c')
        print(result)
        result = False
        return JsonResponse({'redirect_url' : f'../../{param1}/{param2+1}', 'detected':result})
# ------------------------測驗_1------------------------------------

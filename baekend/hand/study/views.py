"""
用來處理使用者引入字卡的時間
"""
import datetime
import base64
import random
import numpy as np
import mediapipe as mp
import cv2
from keras.models import load_model
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


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

model = load_model("study/signDot_with_z.h5")

                # 正解
# BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# MODEL_FILE_PATH = os.path.join(BASE_DIR, 'static', 'models', 'signDot.h5')

def num2alphabet(text):
    """
    將預測結果轉為英文字母
    """
    alphabet = 'ABCDEFGHIKLMNOPQRSTUVWXY'
    return alphabet[text]

def hand_predict(img, correct):
    """
    辨識手的手勢
    """
    correct = str(correct).upper()
    mp_hands = mp.solutions.hands  # mediapipe 偵測手掌方法

    hands_dot = mp_hands.Hands(
        static_image_mode=True,
        model_complexity=1,  # 複雜度越高越準確，但會增加延遲
        max_num_hands=1,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5)

    rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)   #pylint: disable=E1101
    results = hands_dot.process(rgb_img)
    img_h, img_w, _ = img.shape
    if results.multi_hand_landmarks:
        for _, hand_coordinate in zip(results.multi_handedness, results.multi_hand_landmarks):
            all_list = []
            x_list = []
            y_list = []
            for _, point in enumerate(hand_coordinate.landmark):
                # point_x, point_y, _ =
                # int(point.img_x * img_w), int(point.img_y * img_h), int(point.img_z * img_w)
                point_x, point_y = int(point.x * img_w), int(point.y * img_h)
                all_list.append(point_x)
                all_list.append(point_y)
                all_list.append(point.z)
                x_list.append(point_x)
                y_list.append(point_y)
            ## bbox
            xmin, xmax = min(x_list), max(x_list)
            ymin, ymax = min(y_list), max(y_list)
            box_w, box_h = xmax - xmin, ymax - ymin


            if box_w > box_h:
                ymin = int(ymin - (box_w - box_h) / 2)
                box_h = box_w
            else:
                xmin = int(xmin - (box_h - box_w) / 2)
                box_w = box_h
            for i in range(0, len(all_list), 3):
                all_list[i] = (all_list[i] - xmin + 20) / (box_w + 40)
            for j in range(1, len(all_list), 3):
                all_list[j] = (all_list[j] - ymin + 20) / (box_h + 40)

            all_list = np.array(all_list)  # 轉為numpy array
            all_list = all_list.reshape(1, 63)  # reshape
            prediction = model.predict(all_list, verbose=0)  # 輸出的是編碼
            index = np.argmax(prediction)  # 將編碼轉換後才是結果
            text = num2alphabet(index)
            ans = {}
            alphabets = 'ABCDEFGHIKLMNOPQRSTUVWXY'
            count = 0
            for alphabet in alphabets:
                ans[alphabet] = prediction[0][count]
                count = count + 1
            payload = {
                'result': text,
                'result_score': ans[text],
                'correct_score': ans[f'{correct}'],
                'hand_exist' : True,
            }
            return payload
    else:
        print('no hand in image')
        payload = {
                'hand_exist' : False,
            }
        return payload

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
    @swagger_auto_schema(
        operation_summary="測試上傳圖片至模型"
    )
    @root_check
    def get(self, request):
        """
        測試上傳圖片的views
        """
        form = UploadEnglishForm()
        context = {
            'form' : form,
        }
        response  = Response(status=status.HTTP_202_ACCEPTED)
        html =  render(request, './test.html', context=context)
        response.content = html
        return response
    @swagger_auto_schema(
        operation_summary='測試上傳圖片至模型 ',
        # operation_description='我是說明',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'img': openapi.Schema(
                    type=openapi.TYPE_FILE,
                    description='User Name'
                ),
            }
        )
    )
    @root_check
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
        # image_array = cv2.cvtColor(image_array, cv2.COLOR_BGR2RGB) # pylint: disable=E1101
        print(image_array.size)
        result = aaa(img=image_array)
        print("結果一", result)
        result = hand_predict(img=image_array, correct='C')
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
    @swagger_auto_schema(
        operation_summary='已棄用',
    )
    def get(self, request):
        """
        開相機跟傳輸資料基本上只有前端再處理。
        """
        return render(request, 'kamera.html', {})
    @swagger_auto_schema(
        operation_summary='已棄用',
    )
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
        result = hand_predict(img=image_array, correct='c')
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
    @swagger_auto_schema(
        operation_summary='上傳教學圖片 root',
    )
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
    @swagger_auto_schema(
        operation_summary='上傳教學圖片',
        # operation_description='我是說明',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'img': openapi.Schema(
                    type=openapi.TYPE_FILE,
                    description='教學圖片'
                ),
                'des': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description='該資源的描述'
                ),
            }
        )
    )
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
    上傳教學類別
    """
    @swagger_auto_schema(
        operation_summary='上傳教學類別 root',
    )
    @root_check
    def get(self, request):
        """
        獲得上傳教學類別的頁面
        """
        form = UploadTeachTypeForm()
        context = {
            'form' : form,
        }
        response  = Response(status=status.HTTP_202_ACCEPTED)
        html =  render(request, './upload.html', context=context)
        response.content = html
        return response
    @swagger_auto_schema(
        operation_summary='上傳教學類別',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'type': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description='該資源的描述'
                ),
            }
        )
    )
    @root_check
    def post(self, request):
        """
        送出教學類別
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
    @swagger_auto_schema(
            operation_summary='獲得現有的教學資源'
    )
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
    @swagger_auto_schema(
        operation_summary='上傳教學類別',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'redirect_path': openapi.Schema(
                    type=openapi.TYPE_INTEGER,
                    description='所有擁有的資源'
                ),
            }
        )
    )
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
    @swagger_auto_schema(
        operation_summary='獲得詳細的教學資源',
    )
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
    @swagger_auto_schema(
        operation_summary='加入個人字卡',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'card_id': openapi.Schema(
                    type=openapi.TYPE_INTEGER,
                    description='字卡的id'
                ),
            }
        )
    )
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
    @swagger_auto_schema(
        operation_summary='測驗1 字母手勢辨識',
    )
    @loging_check_test
    def get(self, request, param1, param2):
        """
        獲得頁面。
        """
        random_int = random.randint(1, 26)
        alphabet = chr(TeachWordCard.objects.get(id=random_int).id+96)
        # print((TeachWordCard.objects.get(id=random_int).id+96))
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
    @swagger_auto_schema(
        operation_summary='加入個人字卡',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'img': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description='影像'
                ),
                'param1': openapi.Schema(
                    type=openapi.TYPE_INTEGER,
                    description='測驗類別'
                ),
                'param2': openapi.Schema(
                    type=openapi.TYPE_INTEGER,
                    description='題數'
                ),
            }
        )
    )
    def post(self, request, param1, param2):
        """
        使用者送出圖片。
        """
        # print()
        encoded_image = request.data['image']
        # 從 Base64 編碼的字符串中解碼圖片數據
        decoded_image = base64.b64decode(encoded_image.split(',')[1])
        # 將二進制圖片數據轉換為 NumPy 數組
        image_array = np.frombuffer(decoded_image, dtype=np.uint8)
        image_array = cv2.imdecode(image_array, cv2.IMREAD_COLOR) # pylint: disable=E1101
        # image_array = cv2.cvtColor(image_array, cv2.COLOR_BGR2RGB) # pylint: disable=E1101
        cv2.imwrite("./img.png", image_array) # pylint: disable=E1101
        result = hand_predict(img=image_array, correct=request.data['ans'])
        try:
            if result['result_score'] == result['correct_score']:
                print("手勢正確", result['result'])
            else:
                print(request.data['kotae'])
            print(result)
        except KeyError as error_msg:
            print(error_msg, '沒有偵測到手會KeyError')
        payload = {
            'redirect_url' : f'../../{param1}/{param2+1}',
            'detected':result['hand_exist'],
        }
        return JsonResponse(payload)
# ------------------------測驗_1------------------------------------
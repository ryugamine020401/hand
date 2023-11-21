"""
用來處理使用者引入字卡的時間
"""
import datetime
import base64
import random
from io import BytesIO
import numpy as np
import mediapipe as mp
import cv2
from keras.models import load_model
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


from django.shortcuts import render
from django.http import JsonResponse
from django.core.files.uploadedfile import InMemoryUploadedFile

from rest_framework.response import Response
from rest_framework.authentication import get_authorization_header
from rest_framework.views import APIView
from rest_framework import status

from reg.views import decode_access_token
from reg.models import UserIfm
from study.forms import UploadEnglishForm
# from reg.forms import LoginForm, EmailCheckForm
from ifm.models import UseWordCard, UserDefIfm, UserSignLanguageCard
from study.models import TeachWordCard, Test1Ans, Test2, Test2Ans
from study.serializers import UseWordCardSerializer
from hand.settings import NGINX_DOMAIN

import base64
import numpy as np
import cv2
import tempfile
import os
import mediapipe as mp
import tensorflow as tf

# 推理結果轉換的字典
ORD2SIGN = {25: 'blow', 232: 'wait', 48: 'cloud', 23: 'bird', 164: 'owie', 67: 'duck', 143: 'minemy', 134: 'lips', 86: 'flower', 220: 'time', 231: 'vacuum', 8: 'apple', 180: 'puzzle', 144: 'mitten', 216: 'there', 65: 'dry', 195: 'shirt', 165: 'owl', 243: 'yellow', 156: 'not', 249: 'zipper', 45: 'clean', 47: 'closet', 181: 'quiet', 108: 'have', 30: 'brother', 49: 'clown', 41: 'cheek', 54: 'cute', 207: 'store', 196: 'shoe', 235: 'wet', 193: 'see', 70: 'empty', 74: 'fall', 14: 'balloon', 89: 'frenchfries', 80: 'finger', 190: 'same', 52: 'cry', 121: 'hungry', 162: 'orange', 142: 'milk', 97: 'go', 62: 'drawer', 0: 'TV', 6: 'another', 93: 'giraffe', 233: 'wake', 19: 'bee', 13: 'bad', 35: 'can', 191: 'say', 34: 'callonphone', 81: 'finish', 159: 'old', 12: 'backyard', 198: 'sick', 136: 'look', 215: 'that', 24: 'black', 246: 'yourself', 161: 'open', 4: 'alligator', 146: 'moon', 78: 'find', 172: 'pizza', 194: 'shhh', 76: 'fast', 125: 'jacket', 192: 'scissors', 157: 'now', 140: 'man', 206: 'sticky', 127: 'jump', 199: 'sleep', 210: 'sun', 83: 'first', 101: 'grass', 228: 'uncle', 84: 'fish', 51: 'cowboy', 203: 'snow', 66: 'dryer', 102: 'green', 32: 'bug', 150: 'nap', 77: 'feet', 247: 'yucky', 147: 'morning', 189: 'sad', 73: 'face', 169: 'penny', 92: 'gift', 152: 'night', 104: 'hair', 239: 'who', 217: 'think', 31: 'brown', 138: 'mad', 17: 'bed', 63: 'drink', 205: 'stay', 85: 'flag', 223: 'tooth', 11: 'awake', 214: 'thankyou', 120: 'hot', 132: 'like', 237: 'where', 115: 'hesheit', 176: 'potty', 61: 'down', 209: 'stuck', 153: 'no', 110: 'head', 87: 'food', 178: 'pretty', 158: 'nuts', 5: 'animal', 90: 'frog', 21: 'beside', 154: 'noisy', 234: 'water', 236: 'weus', 105: 'happy', 238: 'white', 33: 'bye', 117: 'high', 79: 'fine', 27: 'boat', 3: 'all', 219: 'tiger', 168: 'pencil', 200: 'sleepy', 99: 'grandma', 44: 'chocolate', 109: 'haveto', 182: 'radio', 75: 'farm', 7: 'any', 248: 'zebra', 183: 'rain', 226: 'toy', 60: 'donkey', 133: 'lion', 64: 'drop', 141: 'many', 15: 'bath', 10: 'aunt', 241: 'will', 107: 'hate', 160: 'on', 177: 'pretend', 129: 'kitty', 82: 'fireman', 20: 'before', 59: 'doll', 204: 'stairs', 128: 'kiss', 137: 'loud', 114: 'hen', 135: 'listen', 95: 'give', 242: 'wolf', 55: 'dad', 103: 'gum', 111: 'hear', 186: 'refrigerator', 163: 'outside', 53: 'cut', 229: 'underwear', 173: 'please', 42: 'child', 201: 'smile', 167: 'pen', 245: 'yesterday', 119: 'horse', 171: 'pig', 211: 'table', 72: 'eye', 202: 'snack', 208: 'story', 174: 'police', 9: 'arm', 212: 'talk', 100: 'grandpa', 222: 'tongue', 175: 'pool', 94: 'girl', 230: 'up', 22: 'better', 227: 'tree', 56: 'dance', 46: 'close', 213: 'taste', 43: 'chin', 187: 'ride', 16: 'because', 123: 'if', 38: 'cat', 240: 'why', 37: 'carrot', 58: 'dog', 148: 'mouse', 126: 'jeans', 197: 'shower', 131: 'later', 145: 'mom', 155: 'nose', 244: 'yes', 2: 'airplane', 28: 'book', 26: 'blue', 122: 'icecream', 91: 'garbage', 221: 'tomorrow', 185: 'red', 50: 'cow', 170: 'person', 179: 'puppy', 39: 'cereal', 225: 'touch', 149: 'mouth', 29: 'boy', 218: 'thirsty', 139: 'make', 88: 'for', 96: 'glasswindow', 124: 'into', 184: 'read', 71: 'every', 18: 'bedroom', 151: 'napkin', 68: 'ear', 224: 'toothbrush', 118: 'home', 166: 'pajamas', 113: 'hello', 112: 'helicopter', 130: 'lamp', 188: 'room', 57: 'dirty', 40: 'chair', 106: 'hat', 69: 'elephant', 1: 'after', 36: 'car', 116: 'hide', 98: 'goose'}


mp_holistic = mp.solutions.holistic

holistic = mp_holistic.Holistic(
min_detection_confidence=0.5, min_tracking_confidence=0.5)   # mediapipe全身

def inference(base64_data):
    """
    辨識手語
    """
    # 1. 從Base64字串中解碼數據
    video_data = base64.b64decode(base64_data)

    # 2. 創建一個臨時影片檔案
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4")
    temp_file.write(video_data)
    temp_file.close()

    # 3. 使用OpenCV讀取影片
    cap = cv2.VideoCapture(temp_file.name) # pylint: disable=E1101

    # 4. 逐幀顯示影片
    all_frame = []
    start = 0
    while cap.isOpened():
        ret, image = cap.read()
        if not ret:
            break
        else:
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)  # pylint: disable=E1101
            results = holistic.process(image)  # mediapipe holistic運算

            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR) # pylint: disable=E1101

            frame = []

            if results.face_landmarks and results.pose_landmarks:  # 確認人是否在畫面中
                for a in results.face_landmarks.landmark:  # 臉
                    arr = []
                    arr.append(a.x)
                    arr.append(a.y)
                    arr.append(a.z)
                    frame.append(arr)
                if results.left_hand_landmarks:
                    print('left')
                    start = 1
                    for a in results.left_hand_landmarks.landmark:  # 左手
                        arr = []
                        arr.append(a.x)
                        arr.append(a.y)
                        arr.append(a.z)
                        frame.append(arr)
                else:  # 畫面中沒有左手，座標補-1
                    for i in range(21):
                        frame.append([-1, -1, -1])
                for a in results.pose_landmarks.landmark:  # 姿勢
                    arr = []
                    arr.append(a.x)
                    arr.append(a.y)
                    arr.append(a.z)
                    frame.append(arr)
                if results.right_hand_landmarks:
                    start = 1
                    for a in results.right_hand_landmarks.landmark:  # 右手
                        arr = []
                        arr.append(a.x)
                        arr.append(a.y)
                        arr.append(a.z)
                        frame.append(arr)
                else:  # 畫面中沒有右手，補-1
                    for i in range(21):
                        frame.append([-1, -1, -1])
                if start == 1:
                    all_frame.append(frame)  # 存放這一幀的資料
                    np_all_frame = np.array(all_frame)
                    np_all_frame = np.where(np_all_frame == -1, np.nan, np_all_frame)
                    # print(np_all_frame.shape)
                else:
                    print("start !== 1")
            del frame
    if start == 1:
        # 讀取模型
        interpreter = tf.lite.Interpreter("study/model.tflite")
        # 獲取輸入輸出資料
        input_details = interpreter.get_input_details()
        output_details = interpreter.get_output_details()
        # 輸入資料
        input_data = np_all_frame
        input_data = input_data.astype(np.float32)

        interpreter.resize_tensor_input(input_details[0]['index'], input_data.shape)  # 定義輸入資料大小
        interpreter.allocate_tensors()

        # 輸入資料
        interpreter.set_tensor(input_details[0]['index'], input_data)

        # 推理
        interpreter.invoke()

        # 獲得输出數據
        output_data = interpreter.get_tensor(output_details[0]['index'])

        # 處理輸出數據
        sign = np.argmax(output_data)
        # print(output_data)
        # print(sign)
        # print("inference_result : ", ORD2SIGN.get(sign), f'[{sign}]')

        cap.release()
        cv2.destroyAllWindows() # pylint: disable=E1101
        # 刪除臨時影片
        os.remove(temp_file.name)
        # 回傳推理結果
        return ORD2SIGN.get(sign)
    else:
        print('invalid video')


model = load_model("study/signDot_with_z.h5")

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

# --------------------------------上傳教學圖片------暫時棄用----------------------
class UploadStudyFileView(APIView):
    """
    上傳圖片用的
    """
    @swagger_auto_schema(
        operation_summary='上傳教學圖片 root',
    )
    def get(self, request):
        """
        獲得修改的頁面，已棄用。
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
    def post(self, request):
        """
        送出修改後的資料
        """
        # des = request.data.getlist('describe')
        # img = request.data.getlist('img')

        encoded_image = request.data['img']
        describe = request.data['describe']
        image_binary = base64.b64decode(encoded_image.split(',')[1])
        bytes_io = BytesIO(image_binary)
        image_file = InMemoryUploadedFile(
            file=bytes_io,
            field_name=None,
            name='techimg.png',  # 替換為實際的文件名
            content_type= 'image/png',  # 替換為實際的 MIME 類型
            size=len(image_binary),
            charset=None,
        )
        instance = TeachWordCard()
        instance.img = image_file
        instance.describe = describe
        instance.upload_date = str(datetime.date.today())
        instance.save()
        data = {
            'message':'上傳成功',
        }
        response = JsonResponse(data, status=status.HTTP_200_OK)
        return response

        # for i, item in enumerate(img):
        #     database = TeachWordCard()
        #     database.img = img[i]
        #     database.describe = des[i]
        #     database.upload_date = '2023-08-11'
        #     database.save()
        #     print(database, f'已經儲存到第{i+1}筆資料。{item}')
        # return Response({"successful"})
# ----------------------------上傳教學圖片--------------------------------

# ----------------------------上傳教學類別--------------暫時棄用-------------
# class UploadTeachTypeView(APIView):
#     """
#     上傳教學類別
#     """
#     @swagger_auto_schema(
#         operation_summary='上傳教學類別 root',
#     )
#     @root_check
#     def get(self, request):
#         """
#         獲得上傳教學類別的頁面
#         """
#         form = UploadTeachTypeForm()
#         context = {
#             'form' : form,
#         }
#         response  = Response(status=status.HTTP_202_ACCEPTED)
#         html =  render(request, './upload.html', context=context)
#         response.content = html
#         return response
#     @swagger_auto_schema(
#         operation_summary='上傳教學類別',
#         request_body=openapi.Schema(
#             type=openapi.TYPE_OBJECT,
#             properties={
#                 'type': openapi.Schema(
#                     type=openapi.TYPE_STRING,
#                     description='該資源的描述'
#                 ),
#             }
#         )
#     )
#     @root_check
#     def post(self, request):
#         """
#         送出教學類別
#         """
#         des = request.data.getlist('type')
#         print(des)
#         # for i in range(len(des)):
#         #     print(type(i))
#         #     database = TeachType()
#         #     database.type = des[i]
#         for num, item in enumerate(des):
#             database = TeachType()
#             print(num)
#             database.type = item
#             database.save()
#         return Response({"successful"})

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
        auth = get_authorization_header(request).split()

        try:
            if auth[1] == b'null':
                data = {
                    'message' : '沒有token',
                }
                response = JsonResponse(data, status= status.HTTP_401_UNAUTHORIZED)
                return response
        except IndexError as error_msg:
            print(error_msg, 'TeachingCenterView')
            data = {
                    'message' : '沒有Authorization',
                }
            response = JsonResponse(data, status= status.HTTP_400_BAD_REQUEST)
            return response

        data = {
            'message':'請求成功'
        }
        response = JsonResponse(data, status=status.HTTP_200_OK)
        return response

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
                                            # 字母的id是 1~26 所以id<27
        english_alphabet = TeachWordCard.objects.filter(id__lt=27)
        wordcard = {}
        for instance in english_alphabet:
            wordcard[instance.id] = f'{NGINX_DOMAIN}/api/study'+instance.img.url
        data = {
            'wordcard' : wordcard,
            'message' : "成功獲取資源."
        }

        response = JsonResponse(data, status=status.HTTP_200_OK)

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

    def post(self, request):
        """
        加入使用者個人字卡
        """
        auth = get_authorization_header(request).split()

        try:
            if auth[1] == b'null':
                data = {
                    'message' : '沒有token',
                }
                response = JsonResponse(data, status= status.HTTP_401_UNAUTHORIZED)
                return response

        except IndexError as error_msg:
            print(error_msg, 'TeachingCenterView')
            data = {
                    'message' : '沒有Authorization',
                }
            response = JsonResponse(data, status= status.HTTP_400_BAD_REQUEST)
            return response
        now_time = datetime.datetime.now()
        token = auth[1]
        token_payload = decode_access_token(token)
        try:
            word = chr(int(request.data)+ 96)    # ASCII a是97 card_id是從1~26
            check_multiple = UseWordCard.objects.get(user_id = token_payload['id'], word = word)
            if check_multiple:
                data = {
                'message':'UseWordCardExist'
            }
            response = JsonResponse(data, status=status.HTTP_403_FORBIDDEN)
            return response

        # 查無此資料可以儲存，但會例外所以expect
        except UseWordCard.DoesNotExist as error: # pylint: disable=E1101
            print("目前無此資料，正常儲存。", error)

        # 已經存在的字卡不需要重新儲存
        except UseWordCard.MultipleObjectsReturned as error:    # pylint: disable=E1101
            print("不存", error)
            # 超過兩個以上的情況。
            data = {
                'message':'UseWordCardExist'
            }
            response = JsonResponse(data, status=status.HTTP_403_FORBIDDEN)
            return response

        ser = {
            "user_id" : token_payload['id'],        # a是1 z是26... request data就是id
            "img" : TeachWordCard.objects.get(id = int(request.data)).img,
            "word" : word,    
            "upload_date" : now_time.strftime("%Y-%m-%d"),
        }
        serializer = UseWordCardSerializer(data=ser)

        if serializer.is_valid():
            print("success")
            serializer.save()
        else:
            print(serializer.errors)

        data = {
                'message':'成功加入字卡'
            }
        response = JsonResponse(data, status=status.HTTP_200_OK)
        return response

# ------------------------學習中心_英文------------------------------------

# ------------------------ 學習中心_英文_字卡按鈕 -------------------------
class UserWordCardButtonCheckView(APIView):
    """
    可以讓使用者已加入字卡的字卡按鈕disable
    """
    def get(self, request):
        """
        需要登入狀態，jwt的id可用來辨別使用者
        可以讓使用者已加入字卡的字卡按鈕disable
        """
        auth = get_authorization_header(request).split()
        try:
            if auth[1] == b'null':
                data = {
                    'message' : '沒有token',
                }
                response = JsonResponse(data, status= status.HTTP_401_UNAUTHORIZED)
                return response

        except IndexError as error_msg:
            print(error_msg, 'TeachingCenterView')
            data = {
                    'message' : '沒有Authorization',
                }
            response = JsonResponse(data, status= status.HTTP_400_BAD_REQUEST)
            return response
        token_payload = decode_access_token(auth[1])
        wordarray = UseWordCard.objects.filter(user_id=token_payload['id'])
        no_add_wordcard_buttonenable_list = []
        for word_id in wordarray:
            no_add_wordcard_buttonenable_list.append(ord(word_id.word)-97)
        print(wordarray, no_add_wordcard_buttonenable_list)

        data= {
            'message':'成功獲取未加入字卡的id',
            'enablelist': no_add_wordcard_buttonenable_list,
        }
        response = JsonResponse(data=data, status=status.HTTP_200_OK)
        return response

# ------------------------ 學習中心_英文_字卡按鈕 -------------------------

# ------------------------學習中心_手語------------------------------------
class SignLanguageAPIViews(APIView):
    """
    獲得手語的教學
    包含中英、手語等
    """
    def post(self, request):
        """
        包含數字1 ~ 5 決定一次回傳多少資源 
        """
        print(request.data['pageNum'])
        num = request.data['pageNum']
        resource = Test2.objects.filter(id__range=((num-1)*50+1, 50*num))
        resoyrce_data = {}
        for i in resource:
            # print(i.chinese)
            resoyrce_data[i.vocabularie] = [i.chinese, i.videourl, i.picurl]
        # print(resoyrce_data)
        data = {
            'message' : '獲得資源成功',
            'resource' : resoyrce_data,
        }
        print((num-1)*50+1, 50*num)
        response = JsonResponse(data=data, status=status.HTTP_200_OK)
        return response
# ------------------------學習中心_手語------------------------------------
# ----------------------- 學習中心_手語_加入字卡 --------------------------
class SignLanguageAddCardAPIViews(APIView):
    """
    加入字卡的API Views
    """
    def post(self, request):
        """
        使用者會傳送相關參數
        pic video 的 url
        chinese
        """
        print(request.data)
        auth = get_authorization_header(request).split()
        try:
            if auth[1] == b'null':
                data = {
                    'message' : '沒有token',
                }
                response = JsonResponse(data, status= status.HTTP_401_UNAUTHORIZED)
                return response

        except IndexError as error_msg:
            print(error_msg, 'TeachingCenterView')
            data = {
                    'message' : '沒有Authorization',
                }
            response = JsonResponse(data, status= status.HTTP_400_BAD_REQUEST)
            return response
        
        token_payload = decode_access_token(auth[1])
        print(token_payload['id'])
        user_id = token_payload['id']
        instance = UserSignLanguageCard()
        instance.user_id = UserIfm.objects.get(id=user_id)
        instance.chinese = request.data['chinese']
        instance.videourl = request.data['videourl']
        instance.picurl = request.data['picurl']
        instance.vocabularie = request.data['vocabularie']
        instance.save()
        
        data = {
            'message' : '加入字卡成功',
        }
        response = JsonResponse(data=data, status=status.HTTP_200_OK)
        return response

# ----------------------- 學習中心_手語_加入字卡 --------------------------
# ------------------------ 學習中心_手語_字卡按鈕 -------------------------
class SignLanguageButtonCheckView(APIView):
    """
    可以讓使用者已加入字卡的字卡按鈕disable
    """
    def get(self, request):
        """
        需要登入狀態，jwt的id可用來辨別使用者
        可以讓使用者已加入字卡的字卡按鈕disable
        """
        auth = get_authorization_header(request).split()
        try:
            if auth[1] == b'null':
                data = {
                    'message' : '沒有token',
                }
                response = JsonResponse(data, status= status.HTTP_401_UNAUTHORIZED)
                return response

        except IndexError as error_msg:
            print(error_msg, 'TeachingCenterView')
            data = {
                    'message' : '沒有Authorization',
                }
            response = JsonResponse(data, status= status.HTTP_400_BAD_REQUEST)
            return response
        token_payload = decode_access_token(auth[1])
        wordarray = UserSignLanguageCard.objects.filter(user_id=token_payload['id'])
        no_add_wordcard_buttonenable_list = []
        for word in wordarray:
            no_add_wordcard_buttonenable_list.append(word.vocabularie)
        print(wordarray, no_add_wordcard_buttonenable_list)

        data= {
            'message':'成功獲取已加入字卡的單字名稱',
            'enablelist': no_add_wordcard_buttonenable_list,
        }
        response = JsonResponse(data=data, status=status.HTTP_200_OK)
        return response

# ------------------------ 學習中心_手語_字卡按鈕 -------------------------

# ------------------------測驗_1-------------------------------------------
class TestOneViews(APIView):
    """
    測驗1 英文26字母手勢辨識
    """
    @swagger_auto_schema(
        operation_summary='測驗1 字母手勢辨識',
    )
    def get(self, request, param1, param2):
        """
        獲得頁面。
        """
        auth = get_authorization_header(request).split()

        try:
            if auth[1] == b'null':
                data = {
                    'message' : '沒有token',
                }
                response = JsonResponse(data, status= status.HTTP_401_UNAUTHORIZED)
                return response

        except IndexError as error_msg:
            print(error_msg, 'TeachingCenterView')
            data = {
                    'message' : '沒有Authorization',
                }
            response = JsonResponse(data, status= status.HTTP_400_BAD_REQUEST)
            return response
        token = auth[1]
        token_payload = decode_access_token(token)
        # -------------------- 測驗1 GET -----------------
        if param1 == 1:
            if param2 == 0: # 進到說明頁面
                try:
                    test_instance = Test1Ans.objects.filter(user_id=token_payload['id']).latest('id')
                    data = {
                        'message' : '準備開始測驗...。'
                    }
                    instance = Test1Ans()
                    instance.user_id = UserIfm.objects.get(id=token_payload['id'])
                    if test_instance.kotae_go == '':    # 第五題是空白的代表上次作答沒完成
                        print('上次作答未完成。')
                        test_instance.delete()
                        response = JsonResponse(data, status = status.HTTP_200_OK)
                        return response
                    else:
                        print('已有上次作答，且已完成。開啟新的表格。')
                        instance.save()
                        response = JsonResponse(data, status = status.HTTP_200_OK)
                        return response
                except Test1Ans.DoesNotExist as error_msg: # pylint: disable=E1101
                    print(error_msg)
                    print("進入第0頁 且 從來沒有測驗過。")
                    data = {
                        'message' : '準備開始測驗...。'
                    }

                    instance = Test1Ans()
                    instance.user_id = UserIfm.objects.get(id=token_payload['id'])
                    print(instance)
                    instance.save()
                    response = JsonResponse(data, status = status.HTTP_200_OK)
                    return response
            # 1 以後
            random_int = random.randint(1, 26)
            alphabet = chr(TeachWordCard.objects.get(id=random_int).id+96)
            while 1:
                if (alphabet == 'z' or alphabet == 'j'):
                    random_int = random.randint(1, 26)
                    alphabet = chr(TeachWordCard.objects.get(id=random_int).id+96)
                else:
                    break
            try:
                test_instance = Test1Ans.objects.filter(user_id=token_payload['id']).latest('id')
                print(test_instance)
            except Test1Ans.DoesNotExist as error_msg: # pylint: disable=E1101
                print(error_msg, '755行')
                data = {
                    'message' : '不正確的管道連入網站',
                    'push' : '/study/testtype/1/q0'
                }
                response = JsonResponse(data, status=status.HTTP_302_FOUND)
                return response

            instance_list = ['','kotae_ichi', 'kotae_ni', 'kotae_san', 'kotae_yon', 'kotae_go']
            if param2 > 1:
                if len(getattr(test_instance, instance_list[param2-1])) == 1:
                    print('沒有，跳回普通頁面.')
                    Test1Ans.objects.filter(user_id=token_payload['id']).latest('id').delete()

                    data = {
                        'message' : '不正確的管道連入網站',
                        'push' : '/study/testtype/1/q0'
                    }
                    response = JsonResponse(data, status=status.HTTP_302_FOUND)
                    return response
            if param2 > 5:
                test_instance = Test1Ans.objects.filter(user_id=token_payload['id']).latest('id')
                if test_instance.kotae_go == '':
                    print("沒有東西")
                    test_instance.delete()
                    data = {
                        'message' : '不正確的管道連入網站',
                        'push' : '/study/testtype/1/q0'
                    }
                    response = JsonResponse(data, status=status.HTTP_302_FOUND)
                    return response
                else:
                    # 第五題
                    correct_cnt = 0
                    for value, key in enumerate(vars(test_instance).items()):
                        if 2 <= value <= 6:
                            tmp = key[1].upper()
                            if tmp[0] == tmp[1]:
                                correct_cnt += 1
                        print(key, value)
                        if value == 8:
                            test_instance.cor_rate = correct_cnt*20
                            print(test_instance.cor_rate, correct_cnt*20)
                            test_instance.save()
                    data = {
                        "message :" : '已完成測驗，跳轉至測驗結束畫面。',
                        "push" : "/study/testtype/result",
                        "point": correct_cnt,
                    }
                    response = JsonResponse(data, status=status.HTTP_302_FOUND)
                    return response
            # elif param1 == 2:
            #     data = {
            #         'message':'獲取試驗',
            #     }
            #     response = JsonResponse(data=data, status=status.HTTP_200_OK)
            #     return response

            data = {
                "para1": param1,
                "para2": param2,
                "message :" : 'test',
                "num" : param2+1,
                "mondai" : alphabet,
                # "nextPage" : ,
            }
            instance = Test1Ans.objects.filter(user_id=token_payload['id']).latest('id')
            setattr(instance, instance_list[param2], alphabet)
            instance.save()
            response = JsonResponse(data, status=status.HTTP_200_OK)
            return response
        # ------------------------------------- 測驗1 GET ----------------------------------


        # ------------------------------------- 測驗2 GET ----------------------------------
        elif param1 == 2:
            if param2 == 0: # 進到說明頁面
                try:
                    test_instance = Test2Ans.objects.filter(user_id=token_payload['id']).latest('id')
                    data = {
                        'message' : '準備開始測驗...。'
                    }
                    instance = Test2Ans()
                    instance.user_id = UserIfm.objects.get(id=token_payload['id'])
                    if test_instance.kotae_go == '':    # 第五題是空白的代表上次作答沒完成
                        print('上次作答未完成。')
                        test_instance.delete()
                        response = JsonResponse(data, status = status.HTTP_200_OK)
                        return response
                    else:
                        print('已有上次作答，且已完成。開啟新的表格。')
                        instance.save()
                        response = JsonResponse(data, status = status.HTTP_200_OK)
                        return response
                except Test2Ans.DoesNotExist as error_msg: # pylint: disable=E1101
                    print(error_msg)
                    print("進入第0頁 且 從來沒有測驗過。")
                    data = {
                        'message' : '準備開始測驗...。'
                    }

                    instance = Test2Ans()
                    instance.user_id = UserIfm.objects.get(id=token_payload['id'])
                    print(instance)
                    instance.save()
                    response = JsonResponse(data, status = status.HTTP_200_OK)
                    return response
            random_int = random.randint(1, 250)
            vocabulary = Test2.objects.get(id=random_int).vocabularie
            try:
                test_instance = Test2Ans.objects.filter(user_id=token_payload['id']).latest('id')
                print(test_instance)
            except Test2Ans.DoesNotExist as error_msg: # pylint: disable=E1101
                print(error_msg)
                data = {
                    'message' : '不正確的管道連入網站 870',
                    'push' : '/study/testtype/2/q0'
                }
                response = JsonResponse(data, status=status.HTTP_302_FOUND)
                return response

            instance_list = ['','kotae_ichi', 'kotae_ni', 'kotae_san', 'kotae_yon', 'kotae_go']
            if param2 > 1:
                if len(getattr(test_instance, instance_list[param2-1])) == 1:
                    print('沒有紀錄，跳回說明頁面.')
                    Test2Ans.objects.filter(user_id=token_payload['id']).latest('id').delete()

                    data = {
                        'message' : '不正確的管道連入網站',
                        'push' : '/study/testtype/2/q0'
                    }
                    response = JsonResponse(data, status=status.HTTP_302_FOUND)
                    return response
            if param2 > 5:
                test_instance = Test2Ans.objects.filter(user_id=token_payload['id']).latest('id')
                if test_instance.kotae_go == '':
                    print("網址錯誤")
                    test_instance.delete()
                    data = {
                        'message' : '不正確的管道連入網站',
                        'push' : '/study/testtype/2/q0'
                    }
                    response = JsonResponse(data, status=status.HTTP_302_FOUND)
                    return response
                else:
                    # 第五題
                    correct_cnt = 0
                    for value, key in enumerate(vars(test_instance).items()):
                        print(value, key)
                        if 2 <= value <= 6:
                            tmp = key[1].split(" ")
                            if tmp[0] == tmp[1]:
                                correct_cnt += 1
                        if value == 8:
                            test_instance.cor_rate = correct_cnt*20
                            print(test_instance.cor_rate, correct_cnt*20)
                            test_instance.save()
                    data = {
                        "message :" : '已完成測驗，跳轉至測驗結束畫面。',
                        "push" : "/study/testtype/result2",
                        "point": correct_cnt,
                    }
                    response = JsonResponse(data, status=status.HTTP_302_FOUND)
                    return response

            data = {
                "para1": param1,
                "para2": param2,
                "message :" : 'test',
                "num" : param2+1,
                "mondai" : vocabulary,

            }
            instance = Test2Ans.objects.filter(user_id=token_payload['id']).latest('id')
            setattr(instance, instance_list[param2], vocabulary)
            instance.save()
            response = JsonResponse(data, status=status.HTTP_200_OK)
            return response

            # print('打到2/n')

            # data = {
            #     "para1": param1,
            #     "para2": param2,
            #     "message :" : '測驗2',
            #     "num" : param2+1,
            # }
            # response = JsonResponse(data, status=status.HTTP_200_OK)
            # return response
        # -------------------- 測驗2 GET -----------------
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
        auth = get_authorization_header(request).split()

        try:
            if auth[1] == b'null':
                data = {
                    'message' : '沒有token',
                }
                response = JsonResponse(data, status= status.HTTP_401_UNAUTHORIZED)
                return response

        except IndexError as error_msg:
            print(error_msg, 'TeachingCenterView')
            data = {
                    'message' : '沒有Authorization',
                }
            response = JsonResponse(data, status= status.HTTP_400_BAD_REQUEST)
            return response
        token = auth[1]
        token_payload = decode_access_token(token)
    # ----------------------------- 測驗一 POST --------------------------------
        if param1 == 1:
            encoded_image = request.data['imageBase64']
            # print(request.data.keys(),' 這')
            # print(encoded_image.split(',')[0],' 這')
            # 從 Base64 編碼的字符串中解碼圖片數據
            decoded_image = base64.b64decode(encoded_image.split(',')[1])
            # 將二進制圖片數據轉換為 NumPy 數組
            image_array = np.frombuffer(decoded_image, dtype=np.uint8)
            image_array = cv2.imdecode(image_array, cv2.IMREAD_COLOR) # pylint: disable=E1101
            # image_array = cv2.cvtColor(image_array, cv2.COLOR_BGR2RGB) # pylint: disable=E1101
            cv2.imwrite("./img.png", image_array) # pylint: disable=E1101
            print(request.data['ans'])
            result = hand_predict(img=image_array, correct=request.data['ans'])
            try:
                if result['result_score'] == result['correct_score']:
                    print("手勢正確", result['result'])
                else:
                    print(request.data['ans'])
                print(result)
                # 檢索當前的 ichi 值

                instance_list = ['','kotae_ichi', 'kotae_ni', 'kotae_san', 'kotae_yon', 'kotae_go']
                instance = Test1Ans.objects.filter(user_id=token_payload['id']).latest('id')
                current_value = getattr(instance, instance_list[param2], '')  # 使用getattr，並提供默認值
                # 串聯 'a' 到當前值
                new_value = current_value + result['result']
                # getattr(instance, instance_list[param2]) = result['result']
                setattr(instance, instance_list[param2], new_value)
                instance.save()

            except KeyError as error_msg:
                print(error_msg, '沒有偵測到手會KeyError')
                data = {
                    'message':'沒有偵測到手',
                }
                response = JsonResponse(data, status=status.HTTP_400_BAD_REQUEST)
                return response
            payload = {
                'redirect_url' : f'./{param1}/q{param2+1}',
                'detected':result['hand_exist'],
            }
            return JsonResponse(payload, status=status.HTTP_200_OK)
    # ----------------------------- 測驗一 POST --------------------------------
    # ------------------------ 測驗2 POST ---------------------------------------------
        elif param1 == 2:
            # print('POST到測驗2', request.data['recordedVideo'])
            video_base64 = request.data['recordedVideo'].split(",")[1]
            print('POST到測驗2', inference(video_base64))
            result = inference(video_base64)

            if result is None:
                payload = {
                    'message':'沒有偵測到手'
                    # 'detected':result['hand_exist'],
                }
                return JsonResponse(payload, status=status.HTTP_400_BAD_REQUEST)
            else:
                instance_list = ['','kotae_ichi', 'kotae_ni', 'kotae_san', 'kotae_yon', 'kotae_go']
                instance = Test2Ans.objects.filter(user_id=token_payload['id']).latest('id')
                current_value = getattr(instance, instance_list[param2-1], '')  # 使用getattr，並提供默認值
                # 串聯 'a' 到當前值
                new_value = current_value + " " +result
                # print(instance_list[param2], current_value)
                print("新值", new_value)
                # getattr(instance, instance_list[param2]) = result['result']
                setattr(instance, instance_list[param2-1], new_value)
                instance.save()
                payload = {
                    'redirect_url' : f'./{param1}/q{param2+1}',
                    # 'detected':result['hand_exist'],
                }
                return JsonResponse(payload, status=status.HTTP_200_OK)
        # ------------------------ 測驗2 ---------------------------------------------
# ------------------------測驗_1------------------------------------

# ------------------------ 測驗_1 結算 -----------------------------
class TestOneGetResultAPIView(APIView):
    """
    使用者測驗完成當下 call的API
    用於獲得此次測驗對了幾題
    """
    def get(self, request):
        """
        使用者測驗完成當下 call的API
        用於獲得此次測驗對了幾題
        """
        auth = get_authorization_header(request).split()

        try:
            if auth[1] == b'null':
                data = {
                    'message' : '沒有token',
                }
                response = JsonResponse(data, status= status.HTTP_401_UNAUTHORIZED)
                return response

        except IndexError as error_msg:
            print(error_msg, 'TeachingCenterView')
            data = {
                    'message' : '沒有Authorization',
                }
            response = JsonResponse(data, status= status.HTTP_400_BAD_REQUEST)
            return response
        token = auth[1]
        token_payload = decode_access_token(token)
        test_instance = Test1Ans.objects.filter(user_id=token_payload['id']).latest('id')
        detiallist = []
        for value, key in enumerate(vars(test_instance).items()):
            print(value, key)
            if 2 <= value <= 6:
                detiallist.append(key[1])

        data = {
            'meseage':'成功獲取資源',
            'point': test_instance.cor_rate/20,
            'detial': detiallist,
        }
        response = JsonResponse(data, status=status.HTTP_200_OK)
        return response
# ------------------------ 測驗_1 結算 -----------------------------

# ------------------------ 測驗_2 結算 -----------------------------
class TestOneGetResult2APIView(APIView):
    """
    使用者測驗完成當下 call的API
    用於獲得此次測驗對了幾題
    """
    def get(self, request):
        """
        使用者測驗完成當下 call的API
        用於獲得此次測驗對了幾題
        """
        auth = get_authorization_header(request).split()

        try:
            if auth[1] == b'null':
                data = {
                    'message' : '沒有token',
                }
                response = JsonResponse(data, status= status.HTTP_401_UNAUTHORIZED)
                return response

        except IndexError as error_msg:
            print(error_msg, 'TeachingCenterView')
            data = {
                    'message' : '沒有Authorization',
                }
            response = JsonResponse(data, status= status.HTTP_400_BAD_REQUEST)
            return response
        token = auth[1]
        token_payload = decode_access_token(token)
        test_instance = Test2Ans.objects.filter(user_id=token_payload['id']).latest('id')
        detiallist = []
        for value, key in enumerate(vars(test_instance).items()):
            print(value, key)
            if 2 <= value <= 6:
                detiallist.append(key[1].split(" "))

        data = {
            'meseage':'成功獲取資源',
            'point': test_instance.cor_rate/20,
            'detial': detiallist,
        }
        response = JsonResponse(data, status=status.HTTP_200_OK)
        return response
# ------------------------ 測驗_2 結算 -----------------------------

# ------------------------ 測驗總結算 ------------------------------
class GetAllresultAPIView(APIView):
    """
    可以獲得使用者所有的測驗結果並統整。需要有Accesstoken
    """
    def get(self, request):
        """
        獲得所有測驗的api
        """
        auth = get_authorization_header(request).split()

        try:
            if auth[1] == b'null':
                data = {
                    'message' : '沒有token',
                    'push':'/reg/login',
                }
                response = JsonResponse(data, status= status.HTTP_401_UNAUTHORIZED)
                return response

        except IndexError as error_msg:
            print(error_msg, 'TeachingCenterView')
            data = {
                    'message' : '沒有Authorization',
                    'push':'/reg/login',
                }
            response = JsonResponse(data, status= status.HTTP_400_BAD_REQUEST)
            return response
        token = auth[1]
        token_payload = decode_access_token(token)
        instance = UserDefIfm.objects.get(user_id=token_payload['id'])
        cnt = 0 # 用來計算使用者有幾筆資料
        tmp = 0 # 用來加總使用者分數總和
        cnt2 = 0 # 用來計算使用者有幾筆資料
        tmp2 = 0 # 用來加總使用者分數總和
        for i in Test1Ans.objects.filter(user_id=token_payload['id']):
            if i.kotae_go != '':
                cnt += 1
                tmp += i.cor_rate
        for i in Test2Ans.objects.filter(user_id=token_payload['id']):
            if i.kotae_go != '':
                cnt2 += 1
                tmp2 += i.cor_rate
        # print(tmp/cnt, int((tmp/cnt)/20+1))
        try:
            data = {
                'message':'成功獲取資源',
                'resultScore1':tmp/cnt,
                'resultScore2':tmp2/cnt2,
                'star1':int((tmp/cnt)/20+1),
                'star2':int((tmp2/cnt2)/20+1),
                'headimageurl':f'{NGINX_DOMAIN}/api/ifm{instance.headimg.url}'
            }
        except ZeroDivisionError as error_msg:
            print(error_msg)
            data = {
                'message':'成功獲取資源',
                'resultScore1':0 if cnt == 0 else tmp/cnt,
                'resultScore2':0 if cnt2 == 0 else tmp2/cnt2,
                'star1':1 if cnt == 0 else int((tmp/cnt)/20+1),
                'star2':1 if cnt2 == 0 else int((tmp2/cnt2)/20+1),
                'headimageurl':f'{NGINX_DOMAIN}/api/ifm{instance.headimg.url}'
            }
        response = JsonResponse(data, status=status.HTTP_200_OK)
        return response
# ------------------------ 測驗總結算 ------------------------------

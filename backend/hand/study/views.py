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


from django.shortcuts import render
from django.http import JsonResponse

# from rest_framework.response import Response
from rest_framework.authentication import get_authorization_header
from rest_framework.views import APIView
from rest_framework import status

from reg.views import decode_access_token
from reg.models import UserIfm
# from reg.forms import LoginForm, EmailCheckForm
from ifm.models import UseWordCard, UserDefIfm
from study.models import TeachWordCard, Test1Ans
from study.serializers import UseWordCardSerializer
from hand.settings import NGINX_DOMAIN
# from .hand.prediction import num2alphabet, predict
# def root_check(func):
#     """
#     登入確認，如果沒有找到登入的COOKIES會自度跳轉到登入的頁面。
#     """
#     def wrapper(req, request):
#         print("\n",request, req)
#         token = request.COOKIES.get('access_token')

#         if not token:
#             form = LoginForm()
#             payload = {
#                 "form" : form,
#                 "msg" : "請先登入後再執行該操作。"
#             }
#             response = Response(status=status.HTTP_202_ACCEPTED)
#             html = render(request, 'login.html', payload).content.decode('utf-8')
#             response.content = html
#             return response
#         user = decode_access_token(token)['id']
#         instance = UserIfm.objects.get(email=ROOT_EMAIL)
#         root_id = instance.id
#         if user == root_id:
#             result = func(req, request)
#         else:
#             return Response(status=status.HTTP_403_FORBIDDEN, data = "權限不足")
#         return result
#     return wrapper
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
from study.forms import UploadEnglishForm
from rest_framework.response import Response
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
        english_alphabet = TeachWordCard.objects.all()
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
        # if (param2>6):
        #         data = {
        #             'message' : '不正確的管道連入網站',
        #             'push' : '/study/testtype/1/q0'
        #         }
        #         response = JsonResponse(data, status=status.HTTP_302_FOUND)
        #         return response
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
        if param2 == 0:
            try:
                test_instance = Test1Ans.objects.filter(user_id=token_payload['id']).latest('id')
                print(test_instance)
                if test_instance.kotae_go == '':
                    print("沒有東西")
                    test_instance.delete()
                    data = {
                        'message' : '準備開始測驗...。'
                    }
                else:
                    data = {
                        'message' : '準備開始測驗...。'
                    }
                instance = Test1Ans()
                instance.user_id = UserIfm.objects.get(id=token_payload['id'])
                print(instance)
                instance.save()
                response = JsonResponse(data, status = status.HTTP_200_OK)
                return response
            except Test1Ans.DoesNotExist as error_msg: # pylint: disable=E1101
                print(error_msg)
                data = {
                    'message' : '準備開始測驗...。'
                }

                instance = Test1Ans()
                instance.user_id = UserIfm.objects.get(id=token_payload['id'])
                print(instance)
                instance.save()
                response = JsonResponse(data, status = status.HTTP_200_OK)
                return response

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
        except Test1Ans.DoesNotExist as error_msg: # pylint: disable=E1101
            print(error_msg)
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
                print('第五題')
                
                correct_cnt = 0
                for value, key in enumerate(vars(test_instance).items()):
                    if 2 <= value <= 6:
                        tmp = key[1].upper()
                        if(tmp[0] == tmp[1]):
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
        return JsonResponse(payload)
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

# ------------------------ 測驗總結算 ------------------------------
class getAllresultAPIView(APIView):
    """
    可以獲得使用者所有的測驗結果並統整。需要有Accesstoken
    """
    def get(self, request):
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
        for i in Test1Ans.objects.filter(user_id=token_payload['id']):
            if i.kotae_go != '':
                cnt += 1
                tmp += i.cor_rate    
        # print(tmp/cnt, int((tmp/cnt)/20+1))
        try:
            data = {
                'message':'成功獲取資源',
                'resultScore1':tmp/cnt,
                'start1':int((tmp/cnt)/20+1),
                'headimageurl':f'{NGINX_DOMAIN}/api/ifm{instance.headimg.url}'

            }
        except ZeroDivisionError as error_msg:
            print(error_msg)
            data = {
                'message':'成功獲取資源',
                'resultScore1':0,
                'start1':1,
                'headimageurl':f'{NGINX_DOMAIN}/api/ifm{instance.headimg.url}'

            }
        response = JsonResponse(data, status=status.HTTP_200_OK)
        return response
# ------------------------ 測驗總結算 ------------------------------

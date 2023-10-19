"""
用來處理送到前端的資料
"""
import os
import re
import base64
from io import BytesIO

from django.http import JsonResponse
from django.core.files.uploadedfile import InMemoryUploadedFile

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from rest_framework.authentication import get_authorization_header
from rest_framework.views import APIView
from rest_framework import status

from reg.views import decode_access_token
from reg.serializers import RegisterSerializer
from reg.models import UserIfm
from ifm.serializers import UserDefIfmSerializer
from ifm.models import UserDefIfm, UseWordCard

from hand.settings import NGINX_DOMAIN
from hand.settings import MEDIA_ROOT, MEDIA_URL
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
        headimageurl = f'{NGINX_DOMAIN}/api/ifm{instance.headimg.url}'
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

    def post(self, request):
        """
        送出修改後的資料
        """
        auth = get_authorization_header(request).split()
        try:
            if auth[1] == b'null':
                data = {
                    'message' : '沒有Token',
                }
                response = JsonResponse(data, status = status.HTTP_401_UNAUTHORIZED)
                return response
        except IndexError as error_msg:
            print(error_msg, 'ResetprofileView')
            data = {
                    'message' : '沒有Authorization',
                }
            response = JsonResponse(data, status = status.HTTP_400_BAD_REQUEST)
            return response
        token_payload = decode_access_token(auth[1])
        user_id = token_payload['id']
        try:
            image_name = request.data['imageName']
        except KeyError as error:
            print(error, '使用者上傳裁剪後的頭像')
            image_name = 'crop.png'
        # image_extension_name = request.data['imageNameExtension']
        print(image_name)

        encoded_image = request.data['headimage']

        # print("這裡",encoded_image)
        headimage_binary = base64.b64decode(encoded_image.split(',')[1])
        directory_path = f'{MEDIA_ROOT}/headimage'
        file_name_without_extension = f'avater_{user_id}'
        files_in_directory = os.listdir(directory_path)
        if file_name_without_extension in [os.path.splitext(filename)[0] for filename in files_in_directory]:
            file_to_delete = os.path.join(directory_path, file_name_without_extension)
            print("頭像存在", file_to_delete)
            try:
                os.remove(f'{file_to_delete}.png')
            except FileNotFoundError as error_msg:
                print(error_msg, 'ResetprofileView 不刪除')
            # 權衡之下的結果 物件本身副檔名無所謂 但不固定檔名會導致錯誤
        else:
            print("頭像不存在")

        # 使用 ContentFile 創建一個 BytesIO 對象
        bytes_io = BytesIO(headimage_binary)


        # 正則表達式 匹配到
        # \. 一個點
        # [^.]+ 非點的所有字元多個
        # $ 代表結束
        regex = r'\.[^.]+$'
        # findall 會抓出所有 但只會匹配到一個 所以在list[0]
        # 出來後會是str .png 之類的，所以把點去掉 [1:]
        image_neme_extension = re.findall(regex, image_name)[0]
        # print(image_name+image_extension_name)
        # 創建 InMemoryUploadedFile 對象，模擬上傳的文件
        print(r'')
        image_file = InMemoryUploadedFile(
            file=bytes_io,
            field_name=None,
            name=f'avater_{user_id}.png',  # 替換為實際的文件名
            content_type= f'image/{image_neme_extension[1:]}',  # 替換為實際的 MIME 類型
            size=len(headimage_binary),
            charset=None,
        )
        print(image_file, type(image_file))
        if image_name == 'crop.png':
            instance = UserDefIfm.objects.get(user_id=user_id)
            instance_userifm = UserIfm.objects.get(id=user_id)
            ser1 = {
                "headimg" : image_file,
                "describe" : instance.describe,
                "user_id" : user_id,      # 為了讓序列器is_valid所做的調整，不會更新db的資料
                "score" : 100.0,    # 為了讓序列器is_valid所做的調整，不會更新db的資料
            }
            ser2 = {
                "username" :instance_userifm.username,
                "email" : token_payload['email'],
                "birthday" : instance_userifm.birthday,
                "password" : "nochange",
                "validation_num" : 0,
                "id" : user_id,
            }
        else:
            ser1 = {
                "headimg" : image_file,
                "describe" : request.data["describe"],
                "user_id" : user_id,      # 為了讓序列器is_valid所做的調整，不會更新db的資料
                "score" : 100.0,    # 為了讓序列器is_valid所做的調整，不會更新db的資料
            }
            ser2 = {
                "username" : request.data['username'],
                "email" : token_payload['email'],
                "birthday" : request.data['birthday'],
                "password" : "nochange",
                "validation_num" : 0,
                "id" : user_id,
            }
        change_userdefifm = UserDefIfmSerializer(data=ser1)
        change_userifm = RegisterSerializer(data=ser2)
        if (change_userdefifm.is_valid() and change_userifm.is_valid()):
            print("合法")
            change_userdefifm.update(UserDefIfm.objects.get(user_id=user_id), ser1)
            change_userifm.update1(UserIfm.objects.get(id=user_id), ser2)
        else:
            change_userdefifm.is_valid()
            change_userifm.is_valid()
            print(change_userdefifm.errors,'\n', change_userifm.errors)
        data = {
                    'message' : '成功修改',
                }
        response = JsonResponse(data, status = status.HTTP_200_OK)
        return response

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
        print(request.META)
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
        # wordcard_db = UseWordCard.objects.filter(user_id=ROOT_ID)
        ## ###################### test ######################
        card_url_list = []
        card_url_diec = {}
        for instance in wordcard_db:
            card_url_list.append(NGINX_DOMAIN+'/api/study'+instance.img.url)
            key = instance.word
            value = NGINX_DOMAIN+'/api/study'+instance.img.url
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

"""
用來處理使用者引入字卡的時間
"""
import datetime

from django.shortcuts import render, redirect

from rest_framework.response import Response
# from rest_framework.authentication import get_authorization_header
from rest_framework.views import APIView
from rest_framework import status


from reg.views import decode_access_token
from ifm.models import UseWordCard
from study.models import TeachWordCard, TeachType
from study.forms import UploadEnglishForm, UploadTeachTypeForm
from study.serializers import UseWordCardSerializer
# from hand.settings import SECRET_KEY

# --------------------------------上傳教學圖片--------------------------------
class UploadStudyFileView(APIView):
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
        html =  render(request, './uploadimage.html', context=context)
        response.content = html
        return response

    def post(self, request):
        """
        送出修改後的資料
        """
        des = request.data.getlist('describe')
        img = request.data.getlist('img')
        print(des)
        print(img)
        for i in len(des):
            print(type(i))
            database = TeachWordCard()
            database.img = img[i]
            database.describe = des[i]
            database.upload_date = '2023-08-11'
            database.save()
            print(database)
        return Response({"successful"})

# ----------------------------上傳教學圖片--------------------------------

# ----------------------------上傳教學類別--------------------------------
class UploadTeachTypeView(APIView):
    """
    上傳圖片用的
    """
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
            if (check_multiple):
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

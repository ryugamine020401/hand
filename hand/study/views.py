
"""
用來處理送到前端的資料
"""
from django.shortcuts import render

from rest_framework.response import Response
# from rest_framework.authentication import get_authorization_header
from rest_framework.views import APIView
from rest_framework import status

from study.models import TeachWordCard, TeachType
from study.forms import UploadEnglishForm, UploadTeachTypeForm
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
    讓使用者獲取目前擁有的教學資源    
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
        print(context)
        html = render(request, './english.html', context=context).content.decode('utf-8')
        response.content = html
        return response
# ------------------------學習中心_英文------------------------------------

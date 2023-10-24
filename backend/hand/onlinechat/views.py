"""
用來處理return
"""
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework import status
from onlinechat.models import OlineChatroom

# # -------------- 聊天室 ---------------
# def lobby(request):
#     return render(request, 'lobby.html', {})
# # -------------- 聊天室 ---------------

# -------------- 聊天室獲取前幾筆聊天紀錄 ---------------
class GetLeastChatAPIView(APIView):
    """
    獲得最後五筆的API
    """
    def get(self, request):
        """
        獲得最後五筆的API
        """
        records = OlineChatroom.objects.order_by('id').reverse()[:5]
        print(records, request)
        messagelist = []
        for i in records[::-1]:
            data = {
                'message' : i.message,
                'headimg' : f'/getmedia/{i.message_img}',
                'username' : i.username,
            }
            messagelist.append(data)

        data = {
            'message':'成功獲得資料。',
            'content':messagelist
        }
        response = JsonResponse(data, status=status.HTTP_200_OK)
        return response
# -------------- 聊天室獲取前幾筆聊天紀錄 ---------------

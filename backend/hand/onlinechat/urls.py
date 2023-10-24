from django.urls import path
from onlinechat.views import GetLeastChatAPIView

from . import views
urlpatterns = [
    path('', views.lobby),
    path('api/getmessage', GetLeastChatAPIView.as_view(), name='getleastmesage')
    # path('api/message', MessagePostAPIView.as_view(), name="messageAPI")
]

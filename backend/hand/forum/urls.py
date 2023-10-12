"""
用來給網址的
"""
from django.urls import path

from forum.views import ForumSendAPIView, ForumAPIView, ForumArticalAPIView


urlpatterns = [
    path('api/send/', ForumSendAPIView.as_view(), name='ForumSend'),
    path('api/', ForumAPIView.as_view(), name='Forum'),
    path('api/<int:artical_id>/', ForumArticalAPIView.as_view(), name='ForumArtical'),
]

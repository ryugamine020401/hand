"""
用來給網址的
"""
from django.urls import path

from forum.views import ForumSendView, ForumView, ForumArticalView


urlpatterns = [
    path('send', ForumSendView.as_view(), name='ForumSend'),
    path('', ForumView.as_view(), name='Forum'),
    path('<int:artical_id>/', ForumArticalView.as_view(), name='ForumArtical'),
]

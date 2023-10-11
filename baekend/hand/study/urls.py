"""
用來給網址的
"""
from django.urls import path
from django.conf.urls.static import static

# from study.views import UploadStudyFileView, UploadTeachTypeView
from study.views import TeachingCenterEnglishView, TeachingCenterView
from study.views import UserWordCardButtonCheckView, TestOneViews
from study.views import TestOneGetResultAPIView

from hand.settings import MEDIA_ROOT, MEDIA_URL

urlpatterns = [
    # path('uploadimg', UploadStudyFileView.as_view(), name='UploadStudyImage'),    # 暫時棄用
    # path('uploadteachtype', UploadTeachTypeView.as_view(), name='UploadTeachType'),
    path('api/', TeachingCenterView.as_view(), name='TeachCenterType'),
    path('api/english', TeachingCenterEnglishView.as_view(), name='TeachingCenterEnglish'),
    path('api/test/<int:param1>/<int:param2>/', TestOneViews.as_view(), name='test_one'),
    path('api/wordcardbuttoncheck', UserWordCardButtonCheckView.as_view(), name='UserworlcardCheck'),
    path('api/testoneegetresult', TestOneGetResultAPIView.as_view(), name='TestOneGetResultView'),
]

urlpatterns += static(MEDIA_URL, document_root=MEDIA_ROOT)

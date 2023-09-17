"""
用來給網址的
"""
from django.urls import path
from django.conf.urls.static import static

from study.views import UploadStudyFileView, UploadTeachTypeView
from study.views import TeachingCenterEnglishView, TeachingCenterView, TestUploadImgView
from study.views import TestOneViews
from hand.settings import MEDIA_ROOT, MEDIA_URL

urlpatterns = [
    path('uploadimg', UploadStudyFileView.as_view(), name='UploadStudyImage'),
    path('uploadteachtype', UploadTeachTypeView.as_view(), name='UploadTeachType'),
    path('', TeachingCenterView.as_view(), name='TeachCenterType'),
    path('english', TeachingCenterEnglishView.as_view(), name='TeachingCenterEnglish'),
    path('test', TestUploadImgView.as_view(), name='test'),
    # path('upload_photo', UpLoadImgView.as_view(), name='upload_photo'),
    path('test/<int:param1>/<int:param2>/', TestOneViews.as_view(), name='test_one'),
]

urlpatterns += static(MEDIA_URL, document_root=MEDIA_ROOT)
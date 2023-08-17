"""
用來給網址的
"""
from django.urls import path
from django.conf.urls.static import static

from study.views import UploadStudyFileView, UploadTeachTypeView
from study.views import TeachingCenterEnglishView, TeachingCenterView
from hand.settings import MEDIA_ROOT, MEDIA_URL

urlpatterns = [
    path('uploadimg', UploadStudyFileView.as_view(), name='UploadStudyImage'),
    path('uploadteachtype', UploadTeachTypeView.as_view(), name='UploadTeachType'),
    path('home', TeachingCenterView.as_view(), name='TeachCenterType'),
    path('english', TeachingCenterEnglishView.as_view(), name='TeachingCenterEnglish'),
]

urlpatterns += static(MEDIA_URL, document_root=MEDIA_ROOT)

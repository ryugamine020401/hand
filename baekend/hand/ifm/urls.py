"""
用來給網址的
"""
from django.urls import path
from django.conf.urls.static import static

from ifm.views import ResetprofileView, UserInformationAPIViwe
from ifm.views import UserWordCardAPIView
# from reg.views import index
from hand.settings import MEDIA_ROOT, MEDIA_URL

urlpatterns = [
    # path('', IfmView.as_view(), name='Imformation'),
    path('api/reMeishi', ResetprofileView.as_view(), name='ReMeishi'),
    # path('kado', KadoView.as_view(), name='Kado'),
    path('api/card', UserWordCardAPIView.as_view(), name="UserWordCardAPI"),
    path('api/userinformation', UserInformationAPIViwe.as_view(), name="UserInformationAPI"),
]

urlpatterns += static(MEDIA_URL, document_root=MEDIA_ROOT)

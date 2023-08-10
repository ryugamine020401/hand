"""
用來給網址的
"""
from django.urls import path
from django.conf.urls.static import static

from ifm.views import IfmView
from ifm.views import ResetprofileView
from reg.views import index
from hand.settings import MEDIA_ROOT, MEDIA_URL

urlpatterns = [
    path('api/Meishi', IfmView.as_view(), name='Imformation'),
    path('api/reMeishi', ResetprofileView.as_view(), name='ReMeishi'),
    path('delete', index, name="TEST")
]

urlpatterns += static(MEDIA_URL, document_root=MEDIA_ROOT)

"""
用來給網址的
"""
from django.urls import path
from django.conf.urls.static import static

from ifm.views import IfmView
from ifm.views import ResetprofileView
from ifm.views import KadoView
from reg.views import index
from hand.settings import MEDIA_ROOT, MEDIA_URL

urlpatterns = [
    path('Meishi', IfmView.as_view(), name='Imformation'),
    path('reMeishi', ResetprofileView.as_view(), name='ReMeishi'),
    path('kado', KadoView.as_view(), name='Kado'),
    path('delete', index, name="TEST")
]

urlpatterns += static(MEDIA_URL, document_root=MEDIA_ROOT)

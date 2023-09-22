"""
用來給網址的
"""
from django.urls import path

from billboard.views import BillboardSendAPIView, BillboardView, BillboardArticalView
from billboard.views import RootCheckAPIView


urlpatterns = [
    
    path('', BillboardView.as_view(), name='Billboard'),
    path('<int:artical_id>/', BillboardArticalView.as_view(), name='BillboardArtical'),
    path('api/send', BillboardSendAPIView.as_view(), name='BillboardSendAPI'),
    path('api/rootcheck', RootCheckAPIView.as_view(), name='checkroot'),
]

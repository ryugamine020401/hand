"""
用來給網址的
"""
from django.urls import path

from billboard.views import BillboardSendView, BillboardView, BillboardArticalView


urlpatterns = [
    path('send', BillboardSendView.as_view(), name='BillboardSend'),
    path('', BillboardView.as_view(), name='Billboard'),
    path('<int:artical_id>/', BillboardArticalView.as_view(), name='BillboardArtical'),
]

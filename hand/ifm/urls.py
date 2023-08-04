"""
用來給網址的
"""
from django.urls import path

from ifm.views import IfmView


urlpatterns = [
    path('api/Meishi', IfmView.as_view(), name='Imformation'),
]

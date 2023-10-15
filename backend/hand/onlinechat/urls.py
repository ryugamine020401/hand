from django.urls import path
from .views import MessagePostAPIView
from . import views
urlpatterns = [
    path('', views.lobby),
    path('api/message', MessagePostAPIView.as_view(), name="messageAPI")
]

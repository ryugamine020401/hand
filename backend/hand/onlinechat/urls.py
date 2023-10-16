from django.urls import path

from . import views
urlpatterns = [
    path('', views.lobby),
    # path('api/message', MessagePostAPIView.as_view(), name="messageAPI")
]

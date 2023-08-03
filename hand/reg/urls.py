"""
用來給網址的
"""
from django.urls import path


from reg.views import RegisterView
from reg.views import RegisterValidationView

urlpatterns = [
    path('api/register', RegisterView.as_view(), name='Register'),
    path('api/val', RegisterValidationView.as_view(), name='Validation'),
]

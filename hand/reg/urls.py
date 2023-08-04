"""
用來給網址的
"""
from django.urls import path


from reg.views import RegisterView
from reg.views import RegisterValidationView
from reg.views import LoginView

urlpatterns = [
    path('api/register', RegisterView.as_view(), name='Register'),
    path('api/val', RegisterValidationView.as_view(), name='Validation'),
    path('api/login', LoginView.as_view(), name='Login'),
]

"""
用來給網址的
"""
from django.urls import path


from reg.views import RegisterView, RegisterValidationView
from reg.views import LoginView, PasswordResetViews, EmailValdationView, EmailReSendView
from reg.views import DeleteUserIfmView

urlpatterns = [
    path('register', RegisterView.as_view(), name='Register'),
    path('val', RegisterValidationView.as_view(), name='Validation'),
    path('login', LoginView.as_view(), name='Login'),
    path('repassword', PasswordResetViews.as_view(), name='PasswordReset'),
    path('valemail', EmailValdationView.as_view(), name='EmailValdation'),
    path('api/emailresend', EmailReSendView.as_view(), name='EmailReSend'),
    path('deleteaccount', DeleteUserIfmView.as_view(), name='DeleteUserIfm'),
]

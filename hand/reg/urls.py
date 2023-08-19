"""
用來給網址的
"""
from django.urls import path


from reg.views import RegisterView, RegisterValidationView
from reg.views import LoginView, PasswordResetViews, ResetPasswordAPIView
from reg.views import DeleteUserIfmView, LogoutAPIView
from reg.views import ForgetPasswordView, ForgetPasswordValNumResendAPIView
from reg.views import EmailValdationView, EmailReSendView

urlpatterns = [
    path('register', RegisterView.as_view(), name='Register'),
    path('val', RegisterValidationView.as_view(), name='Validation'),
    path('login', LoginView.as_view(), name='Login'),
    path('repassword', PasswordResetViews.as_view(), name='PasswordReset'),
    path('valemail', EmailValdationView.as_view(), name='EmailValdation'),
    path('forgetpassword', ForgetPasswordView.as_view(), name='ForgetPassword'),
    path('deleteaccount', DeleteUserIfmView.as_view(), name='DeleteUserIfm'),
    path('api/logout', LogoutAPIView.as_view(), name='LogoutAPI'),
    path('api/emailresend', EmailReSendView.as_view(), name='EmailReSend'),
    path('api/forgetpwdvalresend', ForgetPasswordValNumResendAPIView.as_view(), name = 'ForgetPasswordValNumResend'),
    path('api/resetpassword', ResetPasswordAPIView.as_view(), name = 'ResetPasswordAPI'),
]

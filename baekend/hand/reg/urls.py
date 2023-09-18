"""
用來給網址的
"""
from django.urls import path


from reg.views import RegisterView, RegisterValidationView
from reg.views import LoginView, PasswordResetViews, ResetPasswordAPIView
from reg.views import DeleteUserIfmView, LogoutAPIView
from reg.views import ForgetPasswordValNumResendAPIView, ValdataeAPIViwe
from reg.views import EmailReSendView
from reg.views import LoginCheckAPIView

urlpatterns = [
    
    path('api/val', RegisterValidationView.as_view(), name='Validation'),
    path('api/login', LoginView.as_view(), name='Login'),
    path('api/register', RegisterView.as_view(), name='Register'),
    path('api/repassword', PasswordResetViews.as_view(), name='PasswordReset'),
    path('deleteaccount', DeleteUserIfmView.as_view(), name='DeleteUserIfm'),
    path('api/logout', LogoutAPIView.as_view(), name='LogoutAPI'),
    path('api/emailresend', EmailReSendView.as_view(), name='EmailReSend'),
    path('api/forgetpwdvalresend', ForgetPasswordValNumResendAPIView.as_view(), name = 'ForgetPasswordValNumResend'),
    path('api/valdatae', ValdataeAPIViwe.as_view(), name = 'ValdataeAPI'),
    path('api/resetpassword', ResetPasswordAPIView.as_view(), name = 'ResetPasswordAPI'),
    path('api/logincheck', LoginCheckAPIView.as_view(), name='LoginCheckAPI')
]

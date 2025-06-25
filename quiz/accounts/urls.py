from django.urls import path
from accounts.views import UserSignUpView, LogInView, LogOutView


app_name = 'accounts'

urlpatterns = [
    path('signup/', UserSignUpView.as_view(), name='signup'),
    path('login/', LogInView.as_view(), name='login'),
    path('logout/', LogOutView.as_view(), name='logout')
]

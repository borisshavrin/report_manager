from django.urls import path
from users.views import UsersLoginView, UsersRegisterView, UsersProfileView, logout, verify

app_name = 'users'

urlpatterns = [
    path('login/', UsersLoginView.as_view(), name='login'),
    path('register/', UsersRegisterView.as_view(), name='register'),
    path('profile/<int:pk>', UsersProfileView.as_view(), name='profile'),
    path('logout/', logout, name='logout'),
    path('verify/<str:email>/', verify, name='verify'),
]
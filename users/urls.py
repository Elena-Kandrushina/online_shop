from django.urls import path
from users.apps import UsersConfig
from users.views import RegisterView, CustomLogoutView, CustomLoginView

app_name = 'users'

urlpatterns = [
    path('login/', CustomLoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', CustomLogoutView.as_view(template_name='logout.html'), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
]
from django.urls import path
from django.views.generic import TemplateView
from . import views
from user.views import LoginView, RegisterView, log_out

app_name="user"

urlpatterns = [
    path('log_in/', LoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('logout/', views.log_out, name='logout')
]

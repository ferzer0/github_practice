from django.urls import path
from django.views.generic import TemplateView
from . import views
from users.views import RegisterView, LoginView
app_name="users"
urlpatterns = [
    path('log_in', LoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('logout/', views.log_out, name="logout")
]

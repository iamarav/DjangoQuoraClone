from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.HomePage, name='home_page'),
    path('dashboard/', views.DashboardPage, name='dashboard_page'),
    path('dashboard', views.DashboardPage),
    path('user/login/', views.LoginPage, name='login_page'),
    path('user/logout/', views.Logout, name='logout_page'),
    path('user/signup/', views.SignupPage, name='signup_page'),
    path('user/forgot_password/', views.ForgotPassword, name='forgot_password_page'),
    path('user/forgot_password/<action>', views.ForgotPassword, name='forgot_password_action'),
    path('', include('Questions.urls')),

]
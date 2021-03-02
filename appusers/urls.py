from django.urls import path

from . import views

app_name = "appusers"
urlpatterns = [
     
    path("", views.index, name="index"),
    path("account/logout", views.logout_view, name="logout"),
    path("account/register/institution_sign_up", views.institution_app_user_sign_up, name="institution_app_user_sign_up"),
    path("account/register/business", views.business_app_user_sign_up, name="business_app_user_sign_up"),
    path("account/user/login", views.login_business, name="login_business"),
    path("account/user/password/reset", views.password_reset_business, name="password_reset_business"),
]
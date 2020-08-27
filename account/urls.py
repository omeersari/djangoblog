
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('register/', views.register, name='register'),
    path('logout/', views.log_out, name='logout'),
    path('login/', views.log_in, name='login'),
    path('account/', views.account_view, name='account'),


    path("password_reset/", auth_views.PasswordResetView.as_view(
        template_name="account/password_reset.html"), name="password_reset"),

    path("password_reset/done/", auth_views.PasswordResetDoneView.as_view(
        template_name="account/password_reset_done.html"), name="password_reset_done"),

    path("reset/<uidb64>/<token>/", auth_views.PasswordResetConfirmView.as_view(
        template_name="account/password_reset_confirm.html"), name="password_reset_confirm"),

    path("reset/done/", auth_views.PasswordResetCompleteView.as_view(
        template_name="account/password_reset_complete.html"), name="password_reset_complete"),


    path("password_change/", auth_views.PasswordChangeView.as_view(
        template_name="account/password_change.html"), name="password_change"),

    path("password_change/done/", auth_views.PasswordChangeDoneView.as_view(
        template_name="account/password_change_done.html"), name= "password_change_done"),


]


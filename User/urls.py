from django.contrib import admin
from django.urls import path
from . import views
from django.contrib.auth import views as auth_view

urlpatterns = [
    path('sign_up/',views.index,name='sign_up'),
    path('login/', auth_view.LoginView.as_view(template_name='User/login_form.html'), name='login'),
    path('logout/', views.CustomLogout, name='logout'),
]

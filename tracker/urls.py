from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),          # ⭐ Entry point = Login
    path('dashboard/', views.index, name='index'),     # ⭐ Dashboard after login

    path('signup/', views.signup_view, name='signup'),
    path('logout/', views.logout_view, name='logout'),

    path('add/', views.add_application, name='add_application'),
    path('edit/<int:id>/', views.edit_application, name='edit_application'),
    path('delete/<int:id>/', views.delete_application, name='delete_application'),
]




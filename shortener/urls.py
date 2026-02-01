from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', lambda request: views.redirect('dashboard'), name='root'), # Redirect root to dashboard
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('create/', views.create_url, name='create_url'),
    path('edit/<int:pk>/', views.edit_url, name='edit_url'),
    path('delete/<int:pk>/', views.delete_url, name='delete_url'),
    path('qr/<str:short_code>/', views.qr_code_view, name='qr_code'),
    path('<str:short_code>/', views.redirect_url, name='redirect_url'),
]

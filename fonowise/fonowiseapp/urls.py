from django.urls import path
from . import views

app_name = 'fonowiseapp'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('progresso/', views.progresso_view, name='progresso'),
    path('frase/<int:categoria_id>/', views.frase_view, name='frase_view'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
] 
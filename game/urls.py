from django.urls import path
from . import views

app_name = 'game'

urlpatterns = [
    path('', views.play, name='play'),
    path('level/<int:level_number>/', views.play_level, name='play_level'),
    path('validate/', views.validate_solution, name='validate_solution'),
    path('dashboard/', views.user_dashboard, name='dashboard'),
    
    # In-app Admin Panel
    path('admin-panel/', views.admin_panel, name='admin_panel'),
    path('admin-panel/levels/', views.admin_levels, name='admin_levels'),
    path('admin-panel/levels/add/', views.admin_level_add, name='admin_level_add'),
    path('admin-panel/levels/<int:pk>/edit/', views.admin_level_edit, name='admin_level_edit'),
    path('admin-panel/levels/<int:pk>/delete/', views.admin_level_delete, name='admin_level_delete'),
    path('admin-panel/users/', views.admin_users, name='admin_users'),
    path('admin-panel/users/<int:pk>/delete/', views.admin_user_delete, name='admin_user_delete'),
]

from django.contrib import admin
from btp import views
from django.urls import path, include   # 👈 IMPORTANT

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', views.home, name='home'),
   # 👇 TRÈS IMPORTANT
    path('', include('btp.urls')),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # 👇 IMPORTANT : prefix views.
    path('admin-panel/', views.admin_panel, name='admin_panel'),
    path('backup/', views.backup_db, name='backup_db'),
]
from django.urls import path
from . import views

urlpatterns = [

    # =========================
    # 📊 DASHBOARD
    # =========================
    path('', views.dashboard, name='dashboard'),

    # =========================
    # 📄 DEVIS
    # =========================
    path('devis/', views.devis_list, name='devis_list'),
    path('devis/create/', views.create_devis, name='create_devis'),
    path('devis/<int:id>/', views.devis_detail, name='devis_detail'),
    path('devis/<int:id>/pdf/', views.devis_pdf, name='devis_pdf'),

    # =========================
    # 👤 USERS (UI CUSTOM)
    # =========================
    path('users/', views.users_list, name='users_list'),
    path('users/create/', views.create_user, name='create_user'),
    path('users/<int:id>/toggle/', views.toggle_user, name='toggle_user'),
    path('users/<int:id>/delete/', views.delete_user, name='delete_user'),

    # =========================
    # ⚙️ ADMIN PANEL (UI INTERNE)
    # =========================
    path('admin-panel/', views.admin_panel, name='admin_panel'),

    # =========================
    # 💾 BACKUP
    # =========================
    path('backup/', views.backup_db, name='backup_db'),

    path('projets/create/', views.create_projet, name='create_projet'),
    path('projets/', views.projet_list, name='projet_list'),
    path('clients/create/', views.create_client, name='create_client'),
    path('materiaux/', views.materiaux_list, name='materiaux_list'),
    path('materiaux/create/', views.create_materiau, name='create_materiau'),
    
]
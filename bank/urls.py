from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),

    # Donors
    path('donors/', views.donor_list, name='donor_list'),
    path('donors/add/', views.donor_create, name='donor_create'),
    path('donors/<int:pk>/edit/', views.donor_update, name='donor_update'),
    path('donors/<int:pk>/delete/', views.donor_delete, name='donor_delete'),

    # Requests
    path('requests/', views.request_list, name='request_list'),
    path('requests/add/', views.request_create, name='request_create'),
    path('requests/<int:pk>/edit/', views.request_update, name='request_update'),

    # Inventory
    path('inventory/', views.inventory_list, name='inventory_list'),
]

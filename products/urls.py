"""URL paths for the 'products' app (shop)"""
from django.urls import path
from . import views


urlpatterns = [
    path('', views.show_products, name='products'),
    path('<int:product_id>', views.product_details, name='product_details'),
    path('add/', views.add_product, name='add_product'),
    path('edit/<int:product_id>/', views.edit_product, name='edit_product'),
    path(
        'delete/<int:product_id>/', views.delete_product, name='delete_product'
        ),
    path(
        'toggle/<int:product_id>/',
        views.toggle_product_active_status,
        name='toggle_product_active_status'
        ),
]

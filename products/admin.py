from django.contrib import admin
from .models import Category, Product

# Register your models here.
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    '''
    Category model - admin site set up:
    Show all fields in list display
    '''
    list_display = ('friendly_name', 'name')

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    '''
    Product model - admin set up: fields to show in list view,
    Allow filtering by category, new, active, allow search by name,
    Allow editing of is_active flag via list view.
    '''
    list_display = ('name', 'sku', 'category', 'price', 'is_new', 'is_active')
    list_filter = ('category', 'is_new', 'is_active',)
    list_editable = ('is_active',)
    search_fields = ['name', ]
from django.contrib import admin
from .models import Contact, Category

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'phone', 'email', 'created_at', 'show')
    ordering = ('-created_at',)
    search_fields = ('first_name', 'last_name', 'phone', 'email','created_at')
    list_filter = ('created_at', 'show')
    list_per_page = 10
    list_display_links = ('id', 'first_name', 'last_name')
    list_editable = ('phone', 'email', 'show')

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')

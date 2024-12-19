from django.contrib import admin

# Register your models here.

from .models import Category,Sub_Category,Product,Contact_us,Order,Brand,Blog


class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'published_date', 'is_published')  # Customize based on your model fields
    search_fields = ('title', 'content', 'author')  # Enable search functionality
    list_filter = ('is_published', 'published_date')  # Filter by status or date
    ordering = ('-published_date',)  # Order by published date (descending)
    prepopulated_fields = {"slug": ("title",)}  # Auto-generate slug from title (if applicable)


admin.site.register(Category)
admin.site.register(Sub_Category)
admin.site.register(Product)
admin.site.register(Contact_us)
admin.site.register(Order)
admin.site.register(Brand)
admin.site.register(Blog, BlogAdmin)

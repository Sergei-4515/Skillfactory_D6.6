from django.contrib import admin
from .models import Post, Category

# создаём новый класс для представления товаров в админке
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'text')
    list_filter = ('date_in')
    search_fields = ('name', 'category__name')


admin.site.register(Post)
admin.site.register(Category)
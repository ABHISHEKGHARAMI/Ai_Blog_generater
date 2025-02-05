from django.contrib import admin
from .models import BlogPost
# Register your models here.


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ['user','youtube_title','created_at']
    list_filter = ['created_at']
    search_fields = ['created_at','youtube_title']
from django.contrib import admin
from .models import Post, Favorite, Rating, Category, PostOnCategory

# Register your models here.

admin.site.register(Post)
admin.site.register(Favorite)
admin.site.register(Rating)
admin.site.register(Category)
admin.site.register(PostOnCategory)

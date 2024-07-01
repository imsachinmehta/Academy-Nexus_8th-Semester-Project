from django.contrib import admin
from .models import User, Interest, Skill, Post, Comment, Product, Service, Image

# Register your models here.

admin.site.register(User)
admin.site.register(Interest)
admin.site.register(Skill)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Product)
admin.site.register(Service)
admin.site.register(Image)
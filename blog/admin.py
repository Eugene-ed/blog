from django.contrib import admin
from blog.models import Post, Comment, Category, Feedback



#регистрация созданной модели
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Category)
admin.site.register(Feedback)


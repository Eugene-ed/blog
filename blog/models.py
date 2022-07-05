from django.db import models

#опись моделей блога



class Post(models.Model):
    title = models.CharField(
        max_length=256, verbose_name='Title'
    )
    text = models.TextField(
        verbose_name='Text'
    )
    create_date = models.DateTimeField(
        verbose_name='Date of creating', auto_now_add=True
    ) #DateTimeField хранит дату и время
    publish_date = models.DateTimeField(
        verbose_name='Date of publishing', auto_now_add=True
    )
    published_1 = models.BooleanField(
        verbose_name='Published', default=False
    )
    category = models.ForeignKey(
        'Category', on_delete=models.CASCADE, blank=True, null=True
    )
    author = models.ForeignKey (
        "auth.User", on_delete=models.CASCADE, blank=True, null=True
    )

    # def __init__(self, *args, **kwargs) :
    #     super ().__init__ ( args, kwargs )
    #     self.feedbacks = None

    @property
    def rating(self):
        return self.feedbacks.aggregate(models.Avg('rating')).get('rating__avg')

    def __str__(self):
        return f'{self.title}'


class Comment(models.Model):
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE
    )
    # Post-внешний ключ на таблицу пост, on_delete = models.CASCADE- при удалении поста удаляются все комменты
    text = models.TextField(
        verbose_name='Text'
    )
    publish_date = models.DateTimeField(
        verbose_name='Date of publishing', auto_now_add=True
    )
    author = models.ForeignKey(
        "auth.User", on_delete=models.CASCADE
    )

    def __str__(self):
        return f'{self.text}'


class Category (models.Model):
    title = models.CharField(
        max_length=50, unique=True, verbose_name='Name'
    )

    def __str__(self):
        return f'{self.title}'

class Feedback(models.Model):
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='feedbacks'
    )
    # Post-внешний ключ на таблицу пост, on_delete = models.CASCADE- при удалении поста удаляются все комменты

    author = models.ForeignKey(
        "auth.User", on_delete=models.CASCADE
    )

    text = models.TextField(
        verbose_name='Text'
    )
    publish_date = models.DateTimeField(
        verbose_name='Date of publishing', auto_now_add=True
    )
    rating = models.IntegerField(
        verbose_name='Rating', default=3
    )

    def __str__(self):
        return f'{self.text}'
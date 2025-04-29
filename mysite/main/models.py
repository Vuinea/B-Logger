from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    categories = models.ManyToManyField('Category', related_name='posts')

    def __str__(self):
        return self.title


class Favorite(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.user.username} - {self.post.title}"

    class Meta:
        unique_together = ('post', 'user')


class Rating(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.FloatField()

    def __str__(self):
        return f"{self.user.username} - {self.post.title} - {self.rating}"

    class Meta:
        unique_together = ('post', 'user')

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name



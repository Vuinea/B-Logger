from django.db import models
from django.contrib.auth.models import User
import math

# Create your models here.

class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    categories = models.ManyToManyField('Category', related_name='posts')

    def __str__(self):
        return self.title
    
    def get_average_rating(self) -> float:
        ratings = Rating.objects.filter(post=self)
        if ratings.exists():
            return round(sum(rating.rating for rating in ratings) / ratings.count())
        return 0
    
    def get_filled_in_stars(self) -> int:
        """Get the number of filled in stars for the post rating"""
        return math.floor(self.get_average_rating())
    
    def get_half_stars(self):
        """Get the number of half stars for the post rating"""
        return 1 if self.get_average_rating() % 1 >= 0.5 else 0
    
    def get_empty_stars(self):
        """Get the number of empty stars for the post rating"""
        return 5 - self.get_filled_in_stars() - self.get_half_stars()


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



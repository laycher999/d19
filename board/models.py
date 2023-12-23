from django.contrib.auth.models import User
from django.db import models
from tinymce.models import HTMLField

STATUS_CHOICES = [
    ('active', 'Active'),
    ('completed', 'Completed'),
    # Добавьте другие варианты по мере необходимости
]

class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    code_registration = models.CharField(max_length=100)

class Category(models.Model):
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title


class Ad(models.Model):
    title = models.CharField(max_length=100)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ads_created')
    text = HTMLField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    date_create = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    views = models.IntegerField()
    like = models.ManyToManyField(User, through='LikePage', related_name='liked_ads')

    def get_responses(self):
        return Response.objects.filter(ad=self)

class AdCategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    ad = models.ForeignKey(Ad, on_delete=models.CASCADE)


class News(models.Model):
    title = models.CharField(max_length=100)
    text = HTMLField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)


class LikePage(models.Model):
    ad = models.ForeignKey(Ad, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes_given')


class Response(models.Model):
    ad = models.ForeignKey(Ad, on_delete=models.CASCADE)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='responses_sent')
    text = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    user_name = models.CharField(max_length=255, default='admin')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='новый')

    def __str__(self):
        return f'Response from {self.sender.username} to Ad #{self.ad.id}'






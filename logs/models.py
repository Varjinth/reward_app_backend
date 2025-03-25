from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('user', 'User'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user')

    def __str__(self):
        return self.username


class App(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    download_link = models.URLField()
    points = models.IntegerField()

class UserTask(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    app = models.ForeignKey(App, on_delete=models.CASCADE)
    screenshot = models.ImageField(upload_to="screenshots/")
    completed = models.BooleanField(default=False)

    class Meta:
        unique_together = ("user", "app")
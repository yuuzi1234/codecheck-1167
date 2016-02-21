from django.db import models

# Create your models here.
class Projects(models.Model):
    id = models.AutoField(primary_key=True)
    url = models.CharField(max_length=255, null=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

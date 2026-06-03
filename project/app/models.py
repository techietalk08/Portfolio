from django.db import models


from colorfield.fields import ColorField

class Tag(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Blog(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    tag1 = models.TextField()
    tag2 = models.TextField()  

    card_color = ColorField(default="#6c63ff")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Project(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    tag1 = models.TextField()
    tag2 = models.TextField()
    tag3 = models.TextField()
    card_color = ColorField(default="#6c63ff")
    link = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
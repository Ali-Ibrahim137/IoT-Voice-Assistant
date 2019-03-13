from django.db import models


class Text(models.Model):
    text = models.TextField(max_length=1000)
    def __str__(self):
        return self.text

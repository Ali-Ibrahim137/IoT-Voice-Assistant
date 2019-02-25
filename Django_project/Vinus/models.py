from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

class Device(models.Model):
    device_name = models.CharField(max_length=100)
    thinger_username = models.CharField(max_length=100)
    token = models.CharField(max_length=1000)
    is_connected = models.BooleanField()
    user = models.ForeignKey(User, on_delete = models.CASCADE, default=True)

    def __str__(self):
        return self.device_name

    def get_absolute_url(self):
        return reverse('device-detail', kwargs={'pk': self.pk})

class THINGER_API(models.Model):
    thinger_api_name = models.CharField(max_length=100)
    device = models.ForeignKey(Device, on_delete = models.CASCADE, default=True)
    def __str__(self):
        return self.thinger_api_name

class Resources(models.Model):
    resources_name = models.CharField(max_length=100)
    type = models.IntegerField()
    thinger_api = models.ForeignKey(THINGER_API, on_delete = models.CASCADE, default=True)
    def __str__(self):
        return self.resources_name
    # 1 in
    # 2 out
    # 3 in_out
    # 4 null

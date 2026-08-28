from django.db import models


# Create your models here.
class Plan(models.Model):
    name = models.CharField(max_length=100)
    price = models.PositiveIntegerField(default=0)  # Price in Toman
    max_requests_per_month = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.price} Toman - {self.max_requests_per_month} requests/month"

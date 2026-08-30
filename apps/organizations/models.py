import secrets
from django.db import models
from django.conf import settings


class Organization(models.Model):
    name = models.CharField(max_length=255)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="owned_organizations",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


def generate_api_key():
    return f"sk_live_{secrets.token_urlsafe(24)}"


class APIKey(models.Model):
    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name="api_keys",
    )
    key = models.CharField(
        max_length=64, default=generate_api_key, unique=True, editable=False
    )
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    name = models.CharField(max_length=50, default="Default Key")

    def __str__(self):
        return f"{self.organization.name} - {self.name} ({self.key[:10]}...)"

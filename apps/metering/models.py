from django.db import models
from apps.organizations.models import Organization


class UsageRecord(models.Model):
    organization = models.ForeignKey(
        Organization, on_delete=models.CASCADE, related_name="usage_records"
    )
    metric_name = models.CharField(max_length=50, default="api_requests")
    count = models.PositiveIntegerField(default=0)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("organization", "metric_name")

    def __str__(self):
        return f"{self.organization.name} - {self.metric_name}: {self.count}"

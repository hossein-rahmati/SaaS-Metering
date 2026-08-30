from rest_framework import serializers
from apps.plans.models import Plan


class PlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plan
        fields = ['id', 'name', 'price', 'max_requests_per_month']


class UsageSummarySerializer(serializers.Serializer):
    organization_name = serializers.CharField()
    plan_name = serializers.CharField()
    max_requests = serializers.IntegerField()
    used_requests = serializers.IntegerField()
    remaining_requests = serializers.IntegerField()
    status = serializers.CharField()
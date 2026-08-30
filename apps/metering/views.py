from rest_framework.decorators import api_view
from rest_framework.response import Response
from apps.plans.models import Plan
from django.core.cache import cache
from .serializers import PlanSerializer, UsageSummarySerializer


@api_view(["GET"])
def list_plans_api(request):
    plans = Plan.objects.filter(is_active=True)
    serializer = PlanSerializer(plans, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def usage_summary_api(request):
    org = request.organization
    subscription = org.subscription
    plan = subscription.plan

    cache_key = f"usage:org:{org.id}:api_requests"
    used_requests = cache.get(cache_key, 0)
    remaining = max(0, plan.max_requests_per_month - used_requests)

    data = {
        "organization_name": org.name,
        "plan_name": plan.name,
        "max_requests": plan.max_requests_per_month,
        "used_requests": used_requests,
        "remaining_requests": remaining,
        "status": subscription.status,
    }
    serializer = UsageSummarySerializer(data)
    return Response(serializer.data)


@api_view(["GET"])
def sample_service_api(request):
    return Response(
        {
            "message": "Action completed successfully!",
            "organization": request.organization.name,
        }
    )

from django.http import JsonResponse
from apps.organizations.models import Organization
from apps.subscriptions.models import Subscription
from apps.metering.models import UsageRecord


class UsageLimitMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.path.startswith("/api/"):
            return self.get_response(request)

        org_id = request.headers.get("X-Organization-Id")
        if not org_id:
            return JsonResponse(
                {"error": "X-Organization-Id header is required"}, status=400
            )

        try:
            organization = Organization.objects.get(id=org_id)
        except Organization.DoesNotExist:
            return JsonResponse({"error": "Organization not found"}, status=404)

        try:
            subscription = organization.subscription
        except Subscription.DoesNotExist:
            return JsonResponse(
                {"error": "No subscription found for this organization"}, status=403
            )

        if subscription.status != Subscription.Status.ACTIVE:
            return JsonResponse({"error": "Subscription is not active"}, status=403)

        plan = subscription.plan
        usage, _ = UsageRecord.objects.get_or_create(
            organization=organization, metric_name="api_requests"
        )

        if usage.count >= plan.max_requests_per_month:
            return JsonResponse(
                {
                    "error": "Usage limit exceeded for current plan",
                    "limit": plan.max_requests_per_month,
                    "used": usage.count,
                },
                status=429,
            )

        usage.count += 1
        usage.save()

        request.organization = organization

        return self.get_response(request)

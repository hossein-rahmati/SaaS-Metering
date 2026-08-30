from django.http import JsonResponse
from apps.organizations.models import Organization, APIKey
from apps.subscriptions.models import Subscription
from apps.metering.models import UsageRecord


class UsageLimitMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.path.startswith("/api/"):
            return self.get_response(request)

        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return JsonResponse(
                {
                    "error": "Missing or invalid Authorization header. Expected Bearer token."
                },
                status=401,
            )

        api_key = auth_header.split(" ")[1]

        try:
            api_key = APIKey.objects.select_related("organization").get(
                key=api_key, is_active=True
            )
        except APIKey.DoesNotExist:
            return JsonResponse({"error": "Invalid or inactive API key"}, status=401)

        organization = api_key.organization
        

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

from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(["GET"])
def sample_service_api(request):
    return Response(
        {
            "message": "Action completed successfully!",
            "organization": request.organization.name,
        }
    )

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import APIKey
from .serializers import APIKeySerializer


@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def manage_api_keys(request):
    user = request.user
    organization = user.owned_organizations.first()

    if not organization:
        return Response(
            {"detail": "User does not belong to any organization."},
            status=status.HTTP_404_NOT_FOUND,
        )

    if request.method == "GET":
        keys = APIKey.objects.filter(organization=organization, is_active=True)
        serializer = APIKeySerializer(keys, many=True)
        return Response(serializer.data)

    elif request.method == "POST":
        serializer = APIKeySerializer(data=request.data)
        if serializer.is_valid():
            api_key = APIKey.objects.create(
                organization=organization,
                name=serializer.validated_data.get("name", "Default Key"),
            )
            return Response(
                APIKeySerializer(api_key).data, status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def revoke_api_key(request, key_id):
    user = request.user
    organization = user.owned_organizations.first()

    if not organization:
        return Response(
            {"detail": "User does not belong to any organization."},
            status=status.HTTP_404_NOT_FOUND,
        )

    try:
        api_key = APIKey.objects.get(id=key_id, organization=organization)
    except APIKey.DoesNotExist:
        return Response(
            {"detail": "API key not found."}, status=status.HTTP_404_NOT_FOUND
        )

    api_key.is_active = False
    api_key.save()
    return Response(
        {"message": f'API key "{api_key.name}" has been revoked successfully.'}
    )

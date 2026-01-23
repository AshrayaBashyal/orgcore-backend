from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import Company, CompanyInvite
from .serializers import (
    CompanyCreateSerializer,
    InviteCreateSerializer,
    InviteAcceptSerializer
)
from .services import CompanyService


class CompanyCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = CompanyCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        company = CompanyService.create_company(
            owner=request.user,
            **serializer.validated_data
        )

        return Response({"id": company.id, "name": company.name})
    

class InviteCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, company_id):
        serializer = InviteCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        company = Company.objects.get(id=company_id)

        invite = CompanyService.invite_member(
            company=company,
            inviter=request.user,
            **serializer.validated_data
        )

        return Response({"invite_id": invite.id})
    


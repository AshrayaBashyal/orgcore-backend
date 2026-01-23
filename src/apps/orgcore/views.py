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


class InviteCancelView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, company_id, invite_id):
        company = Company.objects.get(id=company_id)
        CompanyService.cancel_invite(company, request.user, invite_id)
        return Response(status=204)


class InviteAcceptView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = InviteAcceptSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        company = CompanyService.accept_invite(
            user=request.user,
            token=serializer.validated_data["token"]
        )

        return Response({"company": company.name})

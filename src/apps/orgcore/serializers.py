from rest_framework import serializers
from .models import Company, CompanyInvite, CompanyMember


class CompanyCreateSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    description = serializers.CharField(required=False, allow_blank=True)


class InviteCreateSerializer(serializers.Serializer):
    email = serializers.EmailField()
    role = serializers.ChoiceField(choices=CompanyMember.ROLE_CHOICES)


class InviteAcceptSerializer(serializers.Serializer):
    token = serializers.UUIDField()
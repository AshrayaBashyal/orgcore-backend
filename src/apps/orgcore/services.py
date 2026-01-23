from django.core.exceptions import PermissionDenied, ValidationError
from django.contrib.auth.models import User
from .models import Company, CompanyMember, CompanyInvite


class CompanyService:

    @staticmethod
    def create_company(owner, name, description=""):
        if Company.objects.filter(name=name).exists():
            raise ValidationError("Company with this name already exists")

        company = Company.objects.create(
            owner=owner,
            name=name,
            description = description
        )

        CompanyMember.objects.create(
            user=owner,
            company=company,
            role=CompanyMember.ADMIN
        )


    @staticmethod
    def invite_member(company, inviter, email, role):
        if not CompanyMember.objects.filter(
            user=inviter,
            company=company,
            role=CompanyMember.ADMIN
        ).exists():
            raise PermissionDenied("Only admins can invite members")

        invite, created = CompanyInvite.objects.get_or_create(
            email=email,
            company=company,
            defaults={"role": role}
        )

        if not created:
            raise ValidationError("Invite already exists")

        # send email async later (Celery)
        return invite

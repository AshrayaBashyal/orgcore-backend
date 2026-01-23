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



        

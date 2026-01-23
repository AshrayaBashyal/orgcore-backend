from django.core.exceptions import PermissionDenied, ValidationError
from django.contrib.auth.models import User
from .models import Company, CompanyMember, CompanyInvite


def require_admin(company, user):
    if not CompanyMember.objects.filter(
        company=company,
        user=user,
        role=CompanyMember.ADMIN
    ).exists():
        raise PermissionDenied("Admin privileges required")


class CompanyService:

    @staticmethod
    def create_company(owner, name, description=""):
        company = Company.objects.create(
            name=name,
            description=description,
            owner=owner
        )

        CompanyMember.objects.create(
            user=owner,
            company=company,
            role=CompanyMember.ADMIN
        )

        return company

    @staticmethod
    def invite_member(company, inviter, email, role):
        require_admin(company, inviter)

        if CompanyMember.objects.filter(
            company=company,
            user__email=email
        ).exists():
            raise ValidationError("User already in company")

        invite, created = CompanyInvite.objects.get_or_create(
            email=email.lower(),
            company=company,
            defaults={"role": role}
        )

        if not created:
            raise ValidationError("Invite already exists")

        return invite

    @staticmethod
    def cancel_invite(company, inviter, invite_id):
        require_admin(company, inviter)

        invite = CompanyInvite.objects.get(
            id=invite_id,
            company=company,
            is_accepted=False
        )
        invite.delete()

    @staticmethod
    def accept_invite(user, token):
        invite = CompanyInvite.objects.filter(
            token=token,
            is_accepted=False
        ).first()

        if not invite:
            raise ValidationError("Invalid invite")

        if invite.email.lower() != user.email.lower():
            raise PermissionDenied("Invite not for this user")

        CompanyMember.objects.create(
            user=user,
            company=invite.company,
            role=invite.role
        )

        invite.is_accepted = True
        invite.save()

        return invite.company

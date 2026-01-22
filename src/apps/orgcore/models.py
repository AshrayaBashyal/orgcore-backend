from django.db import models
from django.contrib.auth.models import User

class Company(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True)
    owner = models.ForeignKey(User, on_delete=models.PROTECT, related_name="owned_companies")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class CompanyMember(models.Model):
    ADMIN = "admin"
    MANAGER = "manager"
    RECRUITER = "recruiter"

    ROLE_CHOICES = [
        (ADMIN, "Admin"),
        (MANAGER, "Manager"),
        (RECRUITER, "Recruiter"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "company")

    def __str__(self):
        return f"{self.user.email} → {self.company.name} ({self.role})"


import uuid

class CompanyInvite(models.Model):
    email = models.EmailField()
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=CompanyMember.ROLE_CHOICES)

    token = models.UUIDField(default=uuid.uuid4, unique=True)
    is_accepted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("email", "company")

    def __str__(self):
        return f"Invite {self.email} → {self.company.name}"

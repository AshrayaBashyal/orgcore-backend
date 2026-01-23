from django.urls import path
from .views import (
    CompanyCreateView,
    InviteCreateView,
    InviteCancelView,
    InviteAcceptView,
)

urlpatterns = [
    path("companies/create/", CompanyCreateView.as_view()),
    path("companies/<int:company_id>/invite/", InviteCreateView.as_view()),
    path("companies/<int:company_id>/invites/<int:invite_id>/cancel/", InviteCancelView.as_view()),
    path("invites/accept/", InviteAcceptView.as_view()),
]

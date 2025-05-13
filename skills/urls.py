from django.urls import path
from .views import (
    SkillListView, SkillDetailView,
    RequestMatchView, MutualMatchesView,
    PendingRequestsView,    # ← add this
    cancel_request,         # ← if you also wired up cancel/accept/decline
    accept_request,
    decline_request,
)

app_name = 'skills'
urlpatterns = [
    path('', SkillListView.as_view(), name='list'),
    path('detail/<int:pk>/', SkillDetailView.as_view(), name='detail'),
    path('request/<int:pk>/<int:helper_pk>/',
         RequestMatchView.as_view(), name='request'),
    path('matches/', MutualMatchesView.as_view(), name='matches'),
    path('pending/', PendingRequestsView.as_view(), name='pending'),
    path('pending/cancel/<int:pk>/', cancel_request, name='cancel_request'),
    path('pending/accept/<int:pk>/', accept_request, name='accept_request'),
    path('pending/decline/<int:pk>/', decline_request, name='decline_request'),
]

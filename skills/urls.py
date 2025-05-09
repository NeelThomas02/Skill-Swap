from django.urls import path
from .views import (
    SkillListView, SkillDetailView,
    RequestMatchView, MutualMatchesView
)

app_name = 'skills'
urlpatterns = [
    path('', SkillListView.as_view(), name='list'),
    path('detail/<int:pk>/', SkillDetailView.as_view(), name='detail'),
    path('request/<int:pk>/<int:helper_pk>/',
         RequestMatchView.as_view(), name='request'),
    path('matches/', MutualMatchesView.as_view(), name='matches'),
]

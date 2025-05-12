from django.urls import path
from .views import VoteView

app_name = 'reputation'
urlpatterns = [
    path('vote/', VoteView.as_view(), name='vote'),
]

# reputation/urls.py
from django.urls import path
from . import views

app_name = 'reputation'

urlpatterns = [
    path('vote/', views.VoteView.as_view(), name='vote'),
    # etc…
]

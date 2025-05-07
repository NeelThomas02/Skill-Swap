# skills/urls.py
from django.urls import path
from . import views

app_name = 'skills'

urlpatterns = [
    path('', views.SkillListView.as_view(), name='list'),
    # etc…
]

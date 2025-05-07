# skills/views.py

from django.views import generic
from .models import Skill

class SkillListView(generic.ListView):
    model = Skill
    template_name = 'skills/list.html'      # points at templates/skills/list.html
    context_object_name = 'skills'          # in the template you'll loop over "skills"

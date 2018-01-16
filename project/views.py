from django.shortcuts import render
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from project.models import Project, Task, ProjectTeam
from project.forms import ProjectForm, TaskFormSet, ProjectTeamFormSet


# Create your views here.
class ProjectList(ListView):
    model = Project
    fields = ['name','desc','start_date','end_date']
	# def get_queryset(self):
	# 	user = self.request.user
	# 	users_project_list = ProjectTeam.objects.filter(user=user).values_list('project', flat=True)
	# 	return Project.objects.filter(id__in=users_project_list)


class ProjectCreate(CreateView):
    model = Project
    fields = ['name','desc','start_date','end_date']


class ProjectUpdate(UpdateView):
    model = Project
    form_class = ProjectForm

    def get_context_data(self, **kwargs):
        context = super(ProjectUpdate, self).get_context_data(**kwargs)
        if self.request.POST:
            context['task_formset'] = TaskFormSet(self.request.POST, instance=self.object, prefix="task")
            context['task_formset'].full_clean()
            context['team_formset'] = ProjectTeamFormSet(self.request.POST, instance=self.object, prefix="team")
            context['team_formset'].full_clean()
        else:
            context['task_formset'] = TaskFormSet(instance=self.object, prefix="task")
            context['team_formset'] = ProjectTeamFormSet(instance=self.object, prefix="team")
        return context 


class ProjectDelete(DeleteView):
    model = Project
    success_url = reverse_lazy('projectList')
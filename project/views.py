from __future__ import print_function
import json
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy, reverse
from django.db import IntegrityError, transaction
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, FormView
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.utils.encoding import force_text
from django.core.serializers.json import DjangoJSONEncoder
from django.core import serializers
from django.http import HttpResponseRedirect, JsonResponse, HttpResponseForbidden
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
            context['team_formset'] = ProjectTeamFormSet(self.request.POST, instance=self.object, prefix="team")
        else:
            context['task_formset'] = TaskFormSet(instance=self.object, prefix="task")
            context['team_formset'] = ProjectTeamFormSet(instance=self.object, prefix="team")
        return context 

    def form_valid(self, form):
        context = self.get_context_data()
        task_formset = context['task_formset']
        team_formset = context['team_formset']
        if team_formset.is_valid() and task_formset.is_valid():
            self.object = form.save()
            task_formset.instance = self.object
            task_formset.save()
            team_formset.instance = self.object
            team_formset.save()
            return redirect(self.success_url)
        else:
            return self.render_to_response(self.get_context_data(form=form))


class ProjectDelete(DeleteView):
    model = Project
    success_url = reverse_lazy('projectList')


# Create your views here.
# class ProjectList(ListView):
#     def get_queryset(self):
#         user = self.request.user
#         users_project_list = ProjectTeam.objects.filter(member=user).values_list('project', flat=True)
#         return Project.objects.filter(id__in=users_project_list)


@login_required
def update_project(request, **kwargs):
    """
    update draft project
    """
    # set variables
    pk = int(kwargs.get('pk'))
    current_project = get_object_or_404(Project, pk=pk)
    #create the formset, specifying the form you want to repeat and the baseformset that holds the validation rules
    if request.method == "POST":
        # populate the project form and the formset
        project_form = ProjectForm(request.POST, instance=current_project)
        team_formset = ProjectTeamFormSet(request.POST, instance=current_project, prefix="team")
        task_formset = TaskFormSet(request.POST, instance=current_project, prefix="task")
        # validate then save each form in the formset
        if project_form.is_valid() and team_formset.is_valid() and task_formset.is_valid():
            team_formset.save()
            task_formset.save()
            project_form.save()
            current_project.update_totals()
            messages.success(request, 'You have updated successfully updated your project.')
            return redirect(reverse('projects:projectList'))
        else:
            messages.error(request, 'An unexpected error occurred. Your project was NOT saved.')

    else:
        project_form = ProjectForm(instance=current_project)
        team_formset = ProjectTeamFormSet(instance=current_project, prefix="team")
        task_formset = TaskFormSet(instance=current_project, prefix="task")

    context = {
        'project' : current_project,
        'project_form' : project_form,
        'team_formset' : team_formset,
        'task_formset' : task_formset,
    }

    return render(request, 'project/project_update_form.html', context)


@login_required
class ProjectDisplay(DetailView):
    model = Project

    def get_context_data(self, **kwargs):
        context = super(ProjectDisplay, self).get_context_data(**kwargs)
        context['form'] = ProjectForm()
        return context


@login_required
def update_project_details(request, **kwargs):
    """
    update project details
    """
    # set variables
    pk = int(kwargs.get('pk'))
    current_project = get_object_or_404(Project, pk=pk)
    
    if request.method == "POST":
        # populate the project form
        project_form = ProjectForm(request.POST, instance=current_project)
        # validate then save form
        if project_form.is_valid():
            project_form.save()
            messages.success(request, 'Success! Your project details have been updated.')
            return redirect(reverse('projects:projectList'))
        else:
            messages.error(request, 'An unexpected error occurred. Project details NOT saved.')

    else:
        project_form = ProjectForm(instance=current_project)

    # add the requested project and form to the context
    context = {
        'project' : current_project,
        'project_form' : project_form,
    }

    return render(request, 'project/project_update_details.html', context)


@login_required
def update_project_tasks(request, **kwargs):
    """
    update project tasks
    """
    # set variables
    pk = int(kwargs.get('pk'))
    current_project = get_object_or_404(Project, pk=pk)
    if request.method == "POST":
        # create and populate formset
        task_formset = TaskFormSet(request.POST, instance=current_project, prefix="task")
        # validate then save each form in the formset
        if task_formset.is_valid():
            task_formset.save()
            messages.success(request, 'You have updated successfully updated your tasks.')
            return redirect(reverse('projects:projectList'))
        else:
            messages.error(request, 'An unexpected error occurred. Task information was NOT saved.')

    else:
        task_formset = TaskFormSet(instance=current_project, prefix="task")

    context = {
        'project' : current_project,
        'task_formset' : task_formset,
    }

    return render(request, 'project/project_update_tasks.html', context)


@login_required
def update_project_team(request, **kwargs):
    """
    update project team
    """
    # set variables
    pk = int(kwargs.get('pk'))
    current_project = get_object_or_404(Project, pk=pk)
    if request.method == "POST":
        # populate the formset
        team_formset = ProjectTeamFormSet(request.POST, instance=current_project, prefix="team")
        # validate then save each form in the formset
        if team_formset.is_valid():
            team_formset.save()
            messages.success(request, 'Success! Team information updated.')
            return redirect(reverse('projects:projectList'))
        else:
            messages.error(request, 'An unexpected error occurred. Your team information was NOT updated.')

    else:
        team_formset = ProjectTeamFormSet(instance=current_project, prefix="team")
        
    context = {
        'project' : current_project,
        'team_formset' : team_formset,
    }

    return render(request, 'project/project_update_team.html', context)


def project_task_list(request):
    project = request.GET.get('project', None)
    """data = {
        'project_tasks': 
    }"""
    project_task_list = dict(tasks = list(Task.active.filter(project=project).values('id', 'title')))
    return JsonResponse(project_task_list)

def get_user_project_list(request):
    #if request.user.is_authenticated:
    users_project_list = ProjectTeam.objects.filter(member=request.user).values_list('project')
    return JsonResponse(dict(projects = list(Project.active.filter(id__in=users_project_list).values('id', 'name'))))



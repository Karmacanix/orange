from django.forms import ModelForm, DateTimeInput, Textarea, DateInput
from django.forms.models import inlineformset_factory
from project.models import Project, ProjectTeam, Task


class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = ('name', 'desc', 'start_date', 'end_date')
        widgets = {
        	'desc': Textarea(attrs={'cols': 40, 'rows': 4}),
             # need to create a validator that prevents a project start date occuring after the end date - if sd gte ed then error 
            'start_date': DateInput(format='%d %b %Y', attrs={'class': 'date-input'}),
            'end_date': DateInput(format='%d %b %Y', attrs={'class': 'date-input'}),
        }


class ProjectTeamForm(ModelForm):

    class Meta:
        model = ProjectTeam
        fields = '__all__'


class TaskForm(ModelForm):

    class Meta:
        model = Task
        fields = '__all__'

TaskFormSet = inlineformset_factory(Project, Task, form=TaskForm, extra=0, can_delete=True, min_num=1)
ProjectTeamFormSet = inlineformset_factory(Project, ProjectTeam, form=ProjectTeamForm, extra=0, can_delete=True, min_num=1)
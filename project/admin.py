from django.contrib import admin
from .models import Project, Task, ProjectTeam

# Register your models here.
class TaskInline(admin.TabularInline):
    model = Task
    fieldsets = [(None,{'fields': ['title', 'project', 'is_active']})]
    extra = 1


class ProjectTeamInline(admin.TabularInline):
	model=ProjectTeam
	fieldsets = [(None,{'fields': ['project','user','is_active','project_rate', 'percent_allocated' ]})]
	extra = 2


class ProjectAdmin(admin.ModelAdmin):
	fieldsets = [
		(None,						{'fields': [('name','desc'), ]}),
		('Project length',			{'fields': [('start_date', 'end_date')]}),
	]
	inlines = [
		TaskInline,
		ProjectTeamInline,
	]
	list_display = ('id', 'name', 'desc', 'start_date', 'end_date')
	search_fields = ['name','desc']


admin.site.register(Project, ProjectAdmin)
import datetime

now = datetime.datetime.now()

from django.db import models
from django.utils import timezone
# Create your models here.
from django.conf import settings
from django.urls import reverse
from django.db import models

# Create your models here.
class Project(models.Model):
	name = models.CharField(max_length=120, verbose_name='Title')
	desc = models.CharField(max_length=300, verbose_name='Purpose')
	start_date = models.DateField(verbose_name='Starts')
	end_date = models.DateField(verbose_name='Ends')
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	
	objects = models.Manager() #the default manager
	
	class Meta:
		ordering = ('created',)

	def __str__(self):
		return self.name

	def get_absolute_url(self):
		return reverse('project-detail', kwargs={'pk': self.pk})

	def days_until_go_live(self):
		until_go = self.end_date - datetime.date.today()
		return until_go.days
	

class ActiveTasks(models.Manager):
	def get_queryset(self):
		return super(ActiveTasks, self).get_queryset().filter(is_active=True)


class Task(models.Model):
	title = models.CharField(max_length=50, blank=False)
	project = models.ForeignKey(Project, on_delete=models.CASCADE)
	is_active = models.BooleanField(default=True)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	
	objects = models.Manager() #the default manager
	active = ActiveTasks() # the published objects manager

	def __str__(self):
		return self.title

	def get_absolute_url(self):
		return reverse('tasks-detail', kwargs={'pk': self.pk})


class ActiveProjectTeam(models.Manager):
	def get_queryset(self):
		return super(ActiveProjectTeam, self).get_queryset().filter(is_active=True)


class ProjectTeam(models.Model):
	project = models.ForeignKey(Project, on_delete=models.CASCADE) # relationship with the project
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE) # choose from the list of users invited to this project by the admins
	is_active = models.BooleanField(default=True) # prevents a user from logging anymore against the project 
	project_rate = models.DecimalField(decimal_places=2, max_digits=6, verbose_name='Project rate') # what they are charged out for on the invoice
	percent_allocated = models.DecimalField(decimal_places=2, max_digits=5, verbose_name='Percent allocated to project') # how much time the individual is allocated to work on this project. 100% = FTE = 40 hours
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	
	objects = models.Manager() #the default manager
	active = ActiveProjectTeam() # the published objects manager
	
	class Meta:
		ordering = ('created',)

	def __str__(self):
		return str(self.id)

	def get_absolute_url(self):
		return reverse('project-team-detail', kwargs={'pk': self.pk})
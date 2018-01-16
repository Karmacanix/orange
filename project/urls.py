from django.conf import settings
from django.conf.urls import url

from project.views import ProjectList, ProjectCreate, ProjectUpdate, ProjectDelete
from project.views import update_project, project_task_list, get_user_project_list, update_project_details, update_project_tasks, update_project_team



app_name='project'
urlpatterns = [
   url(r'^$', ProjectList.as_view(), name='projectList'),
   url(r'create/$', ProjectCreate.as_view(), name='projectCreate'),
   url(r'(?P<pk>[0-9]+)/$', ProjectUpdate.as_view(), name='projectUpdate'),
   url(r'(?P<pk>[0-9]+)/delete/$', ProjectDelete.as_view(), name='projectDelete'),
   url(r'^ajax/tasks/$', project_task_list, name='project_task_list'),
   url(r'^ajax/projects/$', get_user_project_list, name='get_user_project_list'),
   #url(r'^(?P<pk>[0-9]+)/', update_project, name='update_project'),
   url(r'^(?P<pk>[0-9]+)/details/', update_project_details, name='update_project_details'),
   url(r'^(?P<pk>[0-9]+)/tasks/', update_project_tasks, name='update_project_tasks'),
   url(r'^(?P<pk>[0-9]+)/team/', update_project_team, name='update_project_team'),
]



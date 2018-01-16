from django.conf import settings
from django.conf.urls import url

from project.views import ProjectList, ProjectCreate, ProjectUpdate, ProjectDelete


app_name='project'
urlpatterns = [
   url(r'^$', ProjectList.as_view(), name='projectList'),
   url(r'create/$', ProjectCreate.as_view(), name='projectCreate'),
   url(r'(?P<pk>[0-9]+)/$', ProjectUpdate.as_view(), name='projectUpdate'),
   url(r'(?P<pk>[0-9]+)/delete/$', ProjectDelete.as_view(), name='projectDelete'),
]



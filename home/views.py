from django.shortcuts import render
from django.contrib.auth.models import User
from django.views.generic import DetailView

# Create your views here.
class ProfileView(DetailView):
	template_name = "registration/profile.html"
	model = User

	def get_object(self, queryset=None):
		pk = self.request.user.username
		return User.objects.get(username=pk)


from django.shortcuts import render,redirect
from django.views import generic
from django.views.generic import View
from django.views.generic.edit import CreateView,UpdateView,DeleteView
from .forms import UserForm,UpdateUserForm,UpdateProfileForm,CreatePost
from django.http import HttpResponse 
from django.contrib.auth import authenticate,login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from .models import User,Following,Follower
from django.urls import reverse




def index(request):
	return render(request,'core/index.html')

@login_required
def profile(request, username):
	
	if request.method == 'POST':
		u_form = UpdateUserForm(request.POST,instance=request.user)
		p_form = UpdateProfileForm(request.POST, request.FILES, instance=request.user.profile)
		

		if u_form.is_valid() and p_form.is_valid():
			uname = u_form.cleaned_data['username']

			u_form.save()
			p_form.save()
			u_name = User.objects.get(username=uname)
			for peeps in u_name.follower_set.all():
				peeps = User.objects.get(username=peeps)
				a=peeps.following_set.get(following_name = username)
				a.following_name = uname
				a.save()

			for peeps in u_name.following_set.all():
				peeps = User.objects.get(username=peeps)
				a=peeps.follower_set.get(follower_name = username)
				a.follower_name = uname
				a.save()


			messages.success(request,f'Your Profile has been updated!')
			url = reverse('profile', kwargs = {'username' : uname})
			return redirect(url)

	else:
		if username == request.user.username:
			u_form = UpdateUserForm(instance=request.user)
			p_form = UpdateProfileForm(instance=request.user.profile)
			post_form = CreatePost()
			person = User.objects.get(username = username)

			context = {
					'u_form':u_form,
					'p_form':p_form,
					'post_form':post_form,
					'person':person,
			}	
		else:
			person = User.objects.get(username = username)
			already_a_follower=0
			for followers in person.follower_set.all():
				if (followers.follower_name ==  request.user.username):
					already_a_follower=1
					break;

			if already_a_follower==1:
				context = {
						'person':person,
							
					}
			else:
				context = {
						'person':person,
						'f':1,
					}


	return render(request, 'core/profile.html', context )



class UserFormView(View):
	form_class = UserForm
	template_name = 'core/registration_form.html'

	def get(self, request):
		form = self.form_class(None)
		return render(request,self.template_name,{'form':form})

	def post(self, request):
		form = self.form_class(request.POST)

		if form.is_valid():
			user = form.save(commit=False)
			username = form.cleaned_data['username']
			password = form.cleaned_data['password']
			user.set_password(password)
			user.save()

			user = authenticate(username=username,password=password)
			if user is not None:
				if user.is_active:
					login(request, user)
					messages.success(request,f'Account created for {username}!')
					return redirect('core:index')


		return render(request,self.template_name, {'form':form}) 



def followweb(request, username):

	if request.method == 'POST':
		disciple = User.objects.get(username=request.user.username)
		leader = User.objects.get(username=username)
		
		leader.follower_set.create(follower_name = disciple.username)
		disciple.following_set.create(following_name = leader.username)
		url = reverse('profile', kwargs = {'username' : username})
		return redirect(url)
		

def unfollowweb(request, username):

	if request.method == 'POST':
		disciple = User.objects.get(username=request.user.username)
		leader = User.objects.get(username=username)
		
		leader.follower_set.get(follower_name = disciple.username).delete()
		disciple.following_set.get(following_name = leader.username).delete()
		url = reverse('profile', kwargs = {'username' : username})
		return redirect(url)



def welcome(request):
	url = reverse('profile', kwargs = {'username' : request.user.username})
	return redirect(url)



def postweb(request, username):
	if request.method == 'POST':

		post_form = CreatePost(request.POST)
		if post_form.is_valid():
			post_text = post_form.cleaned_data['post_text']
			
			request.user.post_set.create(post_text=post_text)
			
	url = reverse('profile', kwargs = {'username' : username})
	return redirect(url)
	
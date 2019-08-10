from django.shortcuts import render,redirect
from django.views import generic
from django.views.generic import View
from django.views.generic.edit import CreateView,UpdateView,DeleteView
from .forms import UserForm,UpdateUserForm,UpdateProfileForm,CreatePost,CreateComment
from django.http import HttpResponse 
from django.contrib.auth import authenticate,login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from .models import User,Following,Follower,Post
from django.urls import reverse
from django.http import HttpResponseRedirect




def index(request):
	return render(request,'core/index.html')



@login_required
def profile(request, username):
	
	if request.method == 'POST':
		u_form = UpdateUserForm(request.POST,instance=request.user)
		p_form = UpdateProfileForm(request.POST, request.FILES, instance=request.user.profile)
		

		if u_form.is_valid() and p_form.is_valid():

			u_form.save()
			p_form.save()
			

			messages.success(request,f'Your Profile has been updated!')
			url = reverse('profile', kwargs = {'username' : username})
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
				if (followers.follower_user ==  request.user.username):
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
		comment_form = CreateComment()
		context.update({'comment_form':comment_form})

	return render(request, 'core/profile.html', context)



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
	if request.user.username != username:
		if request.method == 'POST':
			disciple = User.objects.get(username=request.user.username)
			leader = User.objects.get(username=username)
			
			leader.follower_set.create(follower_user = disciple)
			disciple.following_set.create(following_user = leader)
			url = reverse('profile', kwargs = {'username' : username})
			return redirect(url)
		

def unfollowweb(request, username):

	if request.method == 'POST':
		disciple = User.objects.get(username=request.user.username)
		leader = User.objects.get(username=username)
		
		leader.follower_set.get(follower_user = disciple).delete()
		disciple.following_set.get(following_user = leader).delete()
		url = reverse('profile', kwargs = {'username' : username})
		return redirect(url)



def welcome(request):
	url = reverse('profile', kwargs = {'username' : request.user.username})
	return redirect(url)



def postweb(request, username):
	if request.method == 'POST':

		post_form = CreatePost(request.POST,request.FILES)
		if post_form.is_valid():
			post_text = post_form.cleaned_data['post_text']
			post_picture = request.FILES.get('post_picture')
			request.user.post_set.create(post_text=post_text, post_picture = post_picture)
			messages.success(request,f'You have successfully posted!')
			
	url = reverse('profile', kwargs = {'username' : username})
	return redirect(url)


def commentweb(request, username, post_id):
	if request.method == 'POST':

		comment_form = CreateComment(request.POST)
		if comment_form.is_valid():
			comment_text = comment_form.cleaned_data['comment_text']
			user = User.objects.get(username=username)
			post = user.post_set.get(pk=post_id)
			post.comment_set.create(user=request.user,comment_text=comment_text)

			messages.success(request,f'Your Comment has been posted')
			
	url = reverse('profile', kwargs = {'username' : username})
	return redirect(url)
	

def feed(request):

	post_all = Post.objects.order_by('created_at').reverse()

	comment_form = CreateComment()
	context = {
	'post_all' : post_all,
	'comment_form':comment_form,
	}
	return render(request,'core/feed.html',context)
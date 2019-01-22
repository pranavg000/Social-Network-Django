from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):

	user = models.OneToOneField(User, on_delete= models.CASCADE)
	profile_photo = models.FileField(default='default.jpg', upload_to='profile_photos')
	status_info = models.CharField(default="Enter status", max_length=1000) 


	def __str__(self):
		return f'{self.user.username} Profile'

class Post(models.Model):
	user = models.ForeignKey(User,on_delete = models.CASCADE)
	post_text = models.CharField(max_length=2000)
	post_picture = models.FileField(default="default.jpg",upload_to='post_picture')




class Following(models.Model):
	user = models.ForeignKey(User,on_delete = models.CASCADE)
	following_name = models.CharField(max_length=265) 

	def __str__(self):
		return self.following_name


class Follower(models.Model):
	user = models.ForeignKey(User,on_delete = models.CASCADE)
	follower_name = models.CharField(max_length=265) 

	def __str__(self):
		return self.follower_name



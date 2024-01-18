from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import AbstractUser,Group,Permission

# Create your models here.
class User(AbstractUser):
    groups = models.ManyToManyField(Group,related_name='custom_user_set',blank=True)
    user_permissions = models.ManyToManyField(Permission,related_name='cutom_user_set',blank=True)


class UserProfile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    profile_pic= models.ImageField(upload_to='profile_photo',blank=True,null=True)
    biography= models.TextField(blank=True)

    def __str__(self):
        return self.user.username
    
class Post(models.Model):
    user = models.ForeignKey(UserProfile,on_delete=models.CASCADE)
    content =models.TextField()
    image=models.ImageField(upload_to='post_image',blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Posted by {self.user.username} - {self.created_at}"
    
class Like(models.Model):
    user =  models.ForeignKey(UserProfile,on_delete=models.CASCADE)
    post = models.ForeignKey(Post,on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} liked {self.post}"    
class Follow(models.Model):
    following =models.ForeignKey(UserProfile,related_name='following',on_delete=models.CASCADE)
    followers =models.ForeignKey(UserProfile,related_name='followers',on_delete=models.CASCADE)

class Comment(models.Model):
    user = models.ForeignKey(UserProfile,on_delete=models.CASCADE)
    post = models.ForeignKey(Post,on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"comment by {self.user.username} on {self.post}"



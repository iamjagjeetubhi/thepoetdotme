from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django_countries.fields import CountryField
from image_cropping import ImageCropField, ImageRatioField
from sorl.thumbnail import ImageField


class Profile(models.Model):
    """
    Define model for user profile with one-to-one relationship with User table.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=20, blank=True)
    country = CountryField(blank=True)
    about = models.TextField(max_length=500, blank=True)
    facebook = models.CharField(max_length=20, blank=True)
    instagram = models.CharField(max_length=20, blank=True)
    twitter = models.CharField(max_length=20, blank=True)
    file = ImageField(upload_to='uploaded_images', blank=True, )
    firstbook = ImageField(upload_to='uploaded_images', blank=True)
    bookname = models.CharField(max_length=200, blank=True)
    bookgenre = models.CharField(max_length=200, blank=True)
    bookurl = models.CharField(max_length=500, blank=True)
    secondbook = ImageField(upload_to='uploaded_images', blank=True)

# Define signals to update user profile whenever we create/update User model.

    @property
    def photo_url(self, default_path="/static/assets/img/faces/face-0.jpg"):
        if self.file and hasattr(self.file, 'url'):
            return self.file.url 
         
        return default_path
        
    @property
    def firstbook_url(self, default_path="/static/assets/img/faces/face-0.jpg"):
        if self.firstbook and hasattr(self.firstbook, 'url'):
            return self.firstbook.url
         
        return default_path


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """
    Create Profile object whenever new User object is created.
    """
    if created:
        Profile.objects.create(user=instance)
import pdb
def save_profile(backend, user, response, *args, **kwargs):
     
    if backend.name == 'facebook':
        #"http://graph.facebook.com/%s/picture?type=large" % response['id']
        #print (user)
        email = response['email']
        user = User.objects.filter(email=email)

        first_name = response.get('first_name')
        last_name = response.get('last_name')
        email = response.get('email')
        
        

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """
    Update Profile object whenever new User object is updated.
    """
    instance.profile.save()



from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django_countries.fields import CountryField
from image_cropping import ImageCropField, ImageRatioField
from sorl.thumbnail import ImageField
from urllib.request import urlopen, HTTPError
from django.template.defaultfilters import slugify

from django.core.files.base import ContentFile

class Profile(models.Model):
    """
    Define model for user profile with one-to-one relationship with User table.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=20, blank=True)
    country = CountryField(blank=True)
    about = models.TextField(max_length=1000, blank=True)
    facebook = models.CharField(max_length=500, blank=True)
    instagram = models.CharField(max_length=20, blank=True)
    twitter = models.CharField(max_length=20, blank=True)
    file = ImageField(upload_to='uploaded_images', blank=True )
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
    def firstbook_url(self, default_path="/static/assets/img/background/bookcover.png"):
        if self.firstbook and hasattr(self.firstbook, 'url'):
            return self.firstbook.url
         
        return default_path


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """
    Create Profile object whenever new User object is created.

    """
    instance.username = instance.username.lower()
    if created:
        Profile.objects.create(user=instance)
import pdb
"""def save_profile(backend, user, response, *args, **kwargs):
     
    if backend.name == 'facebook':
        #"http://graph.facebook.com/%s/picture?type=large" % response['id']
        #print (user)
        email = response['email']
        user = User.objects.filter(email=email)

        first_name = response.get('first_name')
        last_name = response.get('last_name')
        email = response.get('email')"""
def save_profile(backend, user, response, *args, **kwargs):
    #pdb.set_trace()
    
    if user:
        if kwargs['is_new']:
            attrs = {'user': user}
            if backend.name == 'facebook':
                print("new user")
                profile = Profile.objects.get(user = user)
                url = "http://graph.facebook.com/%s/picture?type=large" % response['id']
                avatar = urlopen(url)
                user.profile.file.save(slugify(user.username + " social") + '.jpg', 
                        ContentFile(avatar.read()))                
                user.profile.facebook = response.get('link')
                user.profile.facebook = user.profile.facebook[25:]
                user.profile.save()
            if backend.name == 'google-oauth2':
                print("new user")
                profile = Profile.objects.get(user = user)
                if response.get('image') and response['image'].get('url'):
                    url = response['image'].get('url')
                    url = url.replace("?sz=50","?sz=200")
                    avatar = urlopen(url)
                    user.profile.file.save(slugify(user.username + " social") + '.jpg', 
                        ContentFile(avatar.read())) 
                user.first_name = response['name']['givenName']
                user.last_name = response['name']['familyName']
                user.email = response['emails'][0]['value']
                user.profile.save()

        else:
            print("old user")
            profile = Profile.objects.get(user = user)
            if backend.name == 'facebook':
                #pdb.set_trace()
                if not user.profile.file:
                    url = "http://graph.facebook.com/%s/picture?type=large" % response['id']
                    avatar = urlopen(url)
                    user.profile.file.save(slugify(user.username + " social") + '.jpg', 
                        ContentFile(avatar.read()))
                if not user.profile.facebook:
                    user.profile.facebook = response['link']
                    user.profile.facebook = user.profile.facebook[25:]
                user.profile.save()
                


            if backend.name == 'google-oauth2':
                print("google user")
                if not user.profile.file:
                    if response.get('image') and response['image'].get('url'):
                        url = response['image'].get('url')
                        url = url.replace("?sz=50","?sz=200")
                        avatar = urlopen(url)
                        user.profile.file.save(slugify(user.username + " social") + '.jpg', 
                            ContentFile(avatar.read()))
                #pdb.set_trace()

            user.profile.save()
        """profile = Profile.objects.get(user=user)
        #if not profile.file:
        url = "http://graph.facebook.com/%s/picture?type=large" % response['id']
        avatar = urlopen(url)
        profile.file.save(slugify(user.username + " social") + '.jpg', 
                        ContentFile(avatar.read())) 
        #if not profile.facebook:  
        profile.facebook = response['link']
        profile.facebook = profile.facebook[25:]
        profile.about = response['email']
        profile.save()"""       

        
            

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """
    Update Profile object whenever new User object is updated.
    """

    instance.profile.save()



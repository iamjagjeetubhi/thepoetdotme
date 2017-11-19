from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth.models import User
from .models import Profile
from django.core.files import File
from PIL import Image
from django.forms.widgets import FileInput







class SignupForm(UserCreationForm):
    email = forms.EmailField(max_length=200)

    def clean_email(self):
        email = self.cleaned_data['email'].strip()
        try:
            User.objects.get(email__iexact=email)
            raise forms.ValidationError('email already exists')
        except User.DoesNotExist:
            return email

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')



    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        #if self.fields['username'].error_messages is not None:
        #    attrs['class'] = 'errors'
        self.fields['username'].label = ''
        self.fields['username'].widget.attrs={
            'class':'form-control border-input',
            #'readonly': True
            }

        self.fields['email'].label = ''
        self.fields['email'].widget.attrs={
            'class':'form-control border-input',
            #'readonly': True
            }
        self.fields['first_name'].required = True
        self.fields['first_name'].widget.attrs={
            'class':'form-control border-input',

            }
        self.fields['last_name'].required = True
        self.fields['last_name'].widget.attrs={
            'class':'form-control border-input',

            }

class EditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username','email')

    def __init__(self, *args, **kwargs):
        super(EditForm, self).__init__(*args, **kwargs)
        #if self.fields['username'].error_messages is not None:
        #    attrs['class'] = 'errors'
        self.fields['username'].label = ''
        self.fields['username'].widget.attrs={
            'class':'form-control border-input',
            #'readonly': True
            }

        self.fields['email'].label = ''
        self.fields['email'].widget.attrs={
            'class':'form-control border-input',
            #'readonly': True
            }

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('facebook','instagram','twitter','country', 'about',)
    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        
        
        self.fields['facebook'].widget.attrs={
            'class':'form-control border-input',
            'placeholder': 'username',
            }

        
        self.fields['instagram'].widget.attrs={
            'class':'form-control border-input',
            'placeholder': 'username',
            }

        
        self.fields['twitter'].widget.attrs={
            'class':'form-control border-input',
            'placeholder': 'username',
            }

        self.fields['about'].required = True
        self.fields['about'].widget.attrs={
            'class':'form-control border-input',
            'placeholder': 'Something about you... ',
            'rows':'5',
            'minlength':'200',
	    'maxlength':'1000',

            }

        self.fields['country'].required = True
        self.fields['country'].widget.attrs={
            'class':'form-control',
            #'style':'max-width:90%;',
            
            
            }

class BookFieldsForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('bookname','bookgenre','bookurl',)
    def __init__(self, *args, **kwargs):
        super(BookFieldsForm, self).__init__(*args, **kwargs)
        
        self.fields['bookname'].required = True
        self.fields['bookname'].widget.attrs={
            'class':'form-control border-input',
            }

        self.fields['bookgenre'].required = True
        self.fields['bookgenre'].widget.attrs={
            'class':'form-control border-input',
            }

        

class PhotoForm(forms.ModelForm):
    file = forms.ImageField(widget=forms.FileInput)
    x = forms.FloatField(widget=forms.HiddenInput())
    y = forms.FloatField(widget=forms.HiddenInput())
    width = forms.FloatField(widget=forms.HiddenInput())
    height = forms.FloatField(widget=forms.HiddenInput())
    class Meta:
        model = Profile
        fields = ('file', 'x', 'y', 'width', 'height',)
    widgets = {
        'file': forms.FileInput,
    }
    def __init__(self, *args, **kwargs):
        super(PhotoForm, self).__init__(*args, **kwargs)
        self.fields['file'].label = ''
        self.fields['file'].widget.attrs={
            'class':'upload',

            #'style': 'display:none;',
            }

    def save(self):
        profile = super(PhotoForm, self).save()

        x = self.cleaned_data.get('x')
        y = self.cleaned_data.get('y')
        w = self.cleaned_data.get('width')
        h = self.cleaned_data.get('height')

        image = Image.open(profile.file)
        cropped_image = image.crop((x, y, w+x, h+y))
        resized_image = cropped_image.resize((200, 200), Image.ANTIALIAS)
        resized_image.save(profile.file.path)

        return profile

class PhotoForm1(forms.ModelForm):
    file1 = forms.ImageField(widget=forms.FileInput)
    x = forms.FloatField(widget=forms.HiddenInput())
    y = forms.FloatField(widget=forms.HiddenInput())
    width = forms.FloatField(widget=forms.HiddenInput())
    height = forms.FloatField(widget=forms.HiddenInput())
    class Meta:
        model = Profile
        fields = ('file1', 'x', 'y', 'width', 'height',)
    
    def __init__(self, *args, **kwargs):
        super(PhotoForm1, self).__init__(*args, **kwargs)
        self.fields['file1'].label = ''
        self.fields['file1'].widget.attrs={
            'class':'upload',

            #'style': 'display:none;',
            }

    def save(self):
        profile = super(PhotoForm1, self).save()

        x = self.cleaned_data.get('x')
        y = self.cleaned_data.get('y')
        w = self.cleaned_data.get('width')
        h = self.cleaned_data.get('height')

        image = Image.open(profile.file)
        cropped_image = image.crop((x, y, w+x, h+y))
        resized_image = cropped_image.resize((200, 200), Image.ANTIALIAS)
        resized_image.save(profile.file1.path)

        return profile

class FirstBookForm(forms.ModelForm):
    firstbook = forms.ImageField(widget=forms.FileInput)
    x = forms.FloatField(widget=forms.HiddenInput())
    y = forms.FloatField(widget=forms.HiddenInput())
    width = forms.FloatField(widget=forms.HiddenInput())
    height = forms.FloatField(widget=forms.HiddenInput())
    class Meta:
        model = Profile
        fields = ('firstbook', 'x', 'y', 'width', 'height',)
    widgets = {
        'firstbook': forms.FileInput,
    }
    def __init__(self, *args, **kwargs):
        super(FirstBookForm, self).__init__(*args, **kwargs)
        self.fields['firstbook'].label = ''
        self.fields['firstbook'].widget.attrs={
            'class':'upload',

            #'style': 'display:none;',
            }

    def save(self):
        profile = super(FirstBookForm, self).save()

        x = self.cleaned_data.get('x')
        y = self.cleaned_data.get('y')
        w = self.cleaned_data.get('width')
        h = self.cleaned_data.get('height')

        image = Image.open(profile.firstbook)
        cropped_image = image.crop((x, y, w+x, h+y))
        resized_image = cropped_image.resize((210, 280), Image.ANTIALIAS)
        resized_image.save(profile.firstbook.path)

        return profile

class PasswordChangeForm(PasswordChangeForm):
    class Meta:
        model = User
        fields = ('password',)
        

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, update_session_auth_hash
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.forms import AdminPasswordChangeForm
from django.core.mail import EmailMessage
from django.db import transaction
from django.http import HttpResponse
from django.shortcuts import redirect, render, get_list_or_404, get_object_or_404
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.translation import ugettext_lazy as _
from .forms import ProfileForm, SignupForm, UserForm, PasswordChangeForm, BookFieldsForm, PhotoForm, EditForm, FirstBookForm, PhotoForm1
from .tokens import account_activation_token





def signup(request):
    if request.user.is_authenticated():
        return redirect('view_profile')
    else:
        if request.method == 'POST':
            form = SignupForm(request.POST)
            if form.is_valid():
                user = form.save(commit=False)
                user.is_active = False
                user.save()
                current_site = get_current_site(request)
                subject = 'Activate your accounts.'
                message = render_to_string('accounts/activation_email.html', {
                    'user':user, 'domain':current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': account_activation_token.make_token(user),
                })
                toemail = form.cleaned_data.get('email')
                email = EmailMessage(subject, message, to=[toemail])
                email.send()
                return render(request, 'accounts/activation_pending.html')
        else:
            form = SignupForm()
        return render(request, 'registration/register.html', {'form': form})


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.backend='django.contrib.auth.backends.ModelBackend'
        user.save()
        login(request, user)
        return render(request, 'accounts/activation_completed.html')
    else:
        return HttpResponse('Activation link is invalid!')

def index(request):
    if request.user.is_authenticated:
        return redirect('userpage')
    else:
        return render(request, 'index.html')

@login_required
def userpage(request):
    username = None
    if request.user.profile.about:
       return redirect('view_profile')
    else:
       return redirect('update_profile')

@login_required
def view_profile(request):
    if request.method == 'POST':
        form = PhotoForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect('view_profile')
    else:
        form = PhotoForm(instance=request.user.profile)
    #import facebook
    #graph = facebook.GraphAPI("EAABlXKvAUJIBANIbZB7dOwaYS1PLNUXar32hfpja0ZAR2WBNGiQbBH6lBd8AcPGhm1zNRMnCMobwtCFqSZAPln3AZADuvKy477oubxCqrS3PZCRiLyZAlwhGpOKlP9EOxZAWSnyIB3u8Ogm5DKq7WjXOkI3Q0BOIY0ZD")
    #app_id = '111448692904082' # Obtained from https://developers.facebook.com/
    #app_secret = 'f470893aba8545e2e61bf55c082d09a1' # Obtained from https://developers.facebook.com/

    # Extend the expiration time of a valid OAuth access token.
    #extended_token = graph.extend_access_token(app_id, app_secret)
    #print(extended_token)    
    #post = graph.get_object(id='288577771193880', fields='feed')
    #print(post['feed']['data'][0]['message'])
    return render(request, 'accounts/1view_profile.html',  {'form': form,})

def myprofileview(request, username):
    user = get_object_or_404(User, username = username)
    profilephoto = user.profile.photo_url
    email = user.email
    firstname = user.first_name
    lastname = user.last_name
    countryname = user.profile.country.name
    countryflag = user.profile.country.flag
    about = user.profile.about
    firstbook = user.profile.firstbook
    bookcover = user.profile.firstbook_url
    bookname = user.profile.bookname
    bookgenre = user.profile.bookgenre
    bookurl = user.profile.bookurl
    twitter = user.profile.twitter
    facebook = user.profile.facebook
    instagram = user.profile.instagram
    return render(request, 'accounts/12view_profile.html',{
        'user': user,
        'firstname' : firstname,
        'lastname' : lastname,
        'email': email,
        'countryname' : countryname,
        'countryflag' : countryflag,
        'profilephoto': profilephoto,
        'about' : about,
        'firstbook' : firstbook,
        'bookcover' : bookcover,
        'bookname' : bookname,
        'bookgenre' : bookgenre,
        'bookurl' : bookurl,
        'twitter' : twitter,
        'facebook' : facebook,
        'email' : email,
        'instagram' : instagram,
        })

def save_profile(backend, user, response, *args, **kwargs):
    if backend.name == 'facebook':
        UP=Profile.objects.create(user=user,first_name=response['bio'],email=response['email'],instagram=response['location'],twitter=response['avatar_url'])
        UP.save()

@login_required
@transaction.atomic
def update_profile(request):
    edit_form = None
    first_book = None
  
    if request.method == 'POST' and 'profile' in request.POST:
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, request.FILES, instance=request.user.profile,)
        form = PhotoForm(instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, _('Your profile was successfully updated!'))
            return redirect('view_profile')
        else:
            messages.error(request, _('Please correct the error below.'))
    elif request.method == 'POST':
        form = PhotoForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect('update_profile')
    else:
        user_form = UserForm(instance=request.user)
        edit_form = EditForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)
        form = PhotoForm(instance=request.user.profile)
        first_book = FirstBookForm(instance=request.user.profile)
    return render(request, 'accounts/edit_profile1.html', {
        'user_form': user_form,
        'profile_form': profile_form,
        'edit_form': edit_form,
        'form': form,
        'first_book':first_book,
    })

@login_required
@transaction.atomic
def change_password(request):
    if request.user.has_usable_password():
        PasswordForm = PasswordChangeForm
    else:
        PasswordForm = AdminPasswordChangeForm

    if request.method == 'POST':
        form = PasswordForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('view_profile')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordForm(request.user)
    return render(request, 'registration/password.html', {
        'form': form
    })
@login_required
@transaction.atomic
def first_book(request):
    if request.method == 'POST':
        form = FirstBookForm(request.POST, request.FILES, instance=request.user.profile)
        book_fields_form = BookFieldsForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid(): 
            form.save()
            return redirect('first_book')

        if book_fields_form.is_valid():
            book_fields_form.save()
            messages.success(request, _('Your profile was successfully updated!'))
            return redirect('view_profile')
    else:
        form = FirstBookForm(instance=request.user.profile)
        book_fields_form = BookFieldsForm(instance=request.user.profile)

    return render(request, 'accounts/first_book.html', {
        'form': form,
        'book_fields_form': book_fields_form,
        })

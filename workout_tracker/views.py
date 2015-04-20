from django.shortcuts import render, render_to_response
from django.template import RequestContext
from friendship.models import Friend, Follow
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, HttpResponse
from workout_tracker.forms import TrainerUserForm, ClientUserForm, UserCreateForm, WorkoutForm
from models import Trainer, Client, User, UserInfo
from friendship.models import FriendshipRequest
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.tokens import default_token_generator
from django.template.response import Template


def view_trainer(request, trainer_id):
    trainer = Trainer.objects.get(id=trainer_id)
    return render(request,'trainer_profile.html', {
        "trainer":trainer,
        "owner": False if request.user.is_anonymous() else request.user.user_info.id == trainer.id})


def view_client(request, client_id):
    client = Client.objects.get(id=client_id)
    return render(request,'client_profile.html', {
        "client":client,
        "owner": False if request.user.is_anonymous() else request.user.user_info.id == client.id})


def trainers(request):
    return render(request,'trainers.html', {"trainers":Trainer.objects.all()})    


def clients(request):
    return render(request,'clients.html', {"clients":Client.objects.all()})    


def trainers_clients(request):

    user = {
    "name":"keshk",
    "email":"keshk@gmail.com",
    "phone":"0123456789",
    "height": "170 CM",
    "weight":"67 KG",

    }
    return render(request,'trainer_client.html',{"user":user})   


def clients_trainers(request):

    user = {
    "name":"keshk",
    "email":"keshk@gmail.com",
    "phone":"0123456789",
    "height": "170 CM",
    "weight":"67 KG",

    }
    return render(request,'client_trainer.html',{"user":user})   

   
def provide_trainer_info(request, user=None, register=False):
    # Like before, get the request's context.
    context = RequestContext(request)

    # A boolean value for telling the template whether the registration was successful.
    # Set to False initially. Code changes value to True when registration succeeds.
    registered = False

    # If it's a HTTP POST, we're interested in processing form data.
    if not register and request.method =='POST' :
        # Attempt to grab information from the raw form information.
        # Note that we make use of both UserForm and UserProfileForm.
        user = User.objects.get(pk=request.POST['user_id'])
        trainer = Trainer(user=user)
        trainer_form = TrainerUserForm(request.POST, instance=trainer)
        ##################################################profile_form = userForm(data=request.POST)

        # If the two forms are valid...
        if trainer_form.is_valid():
            # Save the user's form data to the database.
            trainer_form.save()
            # user = trainer_form.save()
            # user_info = request.user.user_info
            user.backend = 'django.contrib.auth.backends.ModelBackend'
            login(request, user)
            return view_trainer(request, user.user_info.id)
            #current_user=Trainer.objects.get(id=request.user.id)
            #return render_to_response('trainer_profile.html', {'current_user': current_user}, context)
            #return render(request, 'trainer_profile.html', {'trainer': current_user.id }) 
            #return view_trainer(request, user_info.id)


            # Now we hash the password with the set_password method.
            # Once hashed, we can update the user object.
            #user.set_password(user.password)
            #user.save()

            # Now sort out the UserProfile instance.
            # Since we need to set the user attribute ourselves, we set commit=False.
            # This delays saving the model until we're ready to avoid integrity problems.
            ##################################################profile = profile_form.save(commit=False)
            ##################################################profile.user = user

            # Did the user provide a profile picture?
            # If so, we need to get it from the input form and put it in the UserProfile model.
            ##################################################if 'picture' in request.FILES:
                ##################################################profile.picture = request.FILES['picture']

            # Now we save the UserProfile model instance.
            ##################################################profile.save()

            # Update our variable to tell the template registration was successful.
            registered = True

        # Invalid form or forms - mistakes or something else?
        # Print problems to the terminal.
        # They'll also be shown to the user.
        #else:
            #print user_form.errors
    else:
        trainer_form = TrainerUserForm(initial={'user':user})
    # Not a HTTP POST, so we render our form using two ModelForm instances.
    # These forms will be blank, ready for user input.
    #else:
        #user_form = CustomUserForm()
        ##################################################profile_form = userForm()

    # Render the template depending on the context.
    return render_to_response(
            'trainer_info.html',
            {'trainer_form': trainer_form, 'user':user, 'registered': registered},
            context)    


def provide_client_info(request, user=None, register=False):
    # Like before, get the request's context.
    context = RequestContext(request)

    # A boolean value for telling the template whether the registration was successful.
    # Set to False initially. Code changes value to True when registration succeeds.
    registered = False

    # If it's a HTTP POST, we're interested in processing form data.
    if not register and request.method == 'POST':
        # Attempt to grab information from the raw form information.
        # Note that we make use of both UserForm and UserProfileForm.
        user = User.objects.get(pk=request.POST['user_id'])
        client = Client(user=user)
        client_form = ClientUserForm(request.POST, instance=client)
        ##################################################profile_form = userForm(data=request.POST)

        # If the two forms are valid...
        if client_form.is_valid():
            # Save the user's form data to the database.
            client_form.save()
            user.backend = 'django.contrib.auth.backends.ModelBackend'
            login(request, user)
            return view_client(request, user.user_info.id) 

            # Now sort out the UserProfile instance.
            # Since we need to set the user attribute ourselves, we set commit=False.
            # This delays saving the model until we're ready to avoid integrity problems.
            ##################################################profile = profile_form.save(commit=False)
            ##################################################profile.user = user

            # Did the user provide a profile picture?
            # If so, we need to get it from the input form and put it in the UserProfile model.
            ##################################################if 'picture' in request.FILES:
                ##################################################profile.picture = request.FILES['picture']

            # Now we save the UserProfile model instance.
            ##################################################profile.save()

            # Update our variable to tell the template registration was successful.
            registered = True

        # Invalid form or forms - mistakes or something else?
        # Print problems to the terminal.
        # They'll also be shown to the user.
        #else:
            #print user_form.errors
    else:
        client_form = ClientUserForm(initial={'user':user})
    # Not a HTTP POST, so we render our form using two ModelForm instances.
    # These forms will be blank, ready for user input.
    #else:
        #user_form = CustomUserForm()
        ##################################################profile_form = userForm()

    # Render the template depending on the context.
    return render_to_response(
            'client_info.html',
            {'client_form': client_form, 'user':user, 'registered': registered},
            context)                                               


def user_login(request):
    # Like before, obtain the context for the user's request.
    context = RequestContext(request)

    # If the request is a HTTP POST, try to pull out the relevant information.
    if request.method == 'POST':
        # Gather the username and password provided by the user.
        # This information is obtained from the login form.
        username = request.POST['username']
        password = request.POST['password']

        # Use Django's machinery to attempt to see if the username/password
        # combination is valid - a User object is returned if it is.
        user = authenticate(username=username, password=password)

        # If we have a User object, the details are correct.
        # If None (Python's way of representing the absence of a value), no user
        # with matching credentials was found.
        if user:
            # Is the account active? It could have been disabled.
            if user.is_active:
                # If the account is valid and active, we can log the user in.
                # We'll send the user back to the homepage.
                login(request, user)
                user_info = request.user.user_info
                if user_info.type == 'trainer':
                    return view_trainer(request, user_info.id)
                else:
                    return view_client(request, user_info.id)

                # return render_to_response('Homepage.html', {}, context)
            else:
                # An inactive account was used - no logging in!
                return HttpResponse("Your workout account is disabled.")
        else:
            # Bad login details were provided. So we can't log the user in.
            print "Invalid login details: {0}, {1}".format(username, password)
            return HttpResponse("Invalid login details supplied.")

    # The request is not a HTTP POST, so display the login form.
    # This scenario would most likely be a HTTP GET.
    else:
        # No context variables to pass to the template system, hence the
        # blank dictionary object...
        
        if request.user.is_anonymous():
            return render_to_response('login.html', {}, context)
        else:
            user_info = request.user.user_info
            if user_info.type == 'trainer':
                return view_trainer(request, user_info.id)
            else:
                return view_client(request, user_info.id) 



def user_logout(request):
    # Since we know the user is logged in, we can now just log them out.
    logout(request)

    # Take the user back to the homepage.
    return HttpResponseRedirect('/login')         


def register(request, user_type=None):
    # Like before, get the request's context.
    context = RequestContext(request)

    # A boolean value for telling the template whether the registration was successful.
    # Set to False initially. Code changes value to True when registration succeeds.
    registered = False

    # If it's a HTTP POST, we're interested in processing form data.
    if request.method == 'POST':
        # Attempt to grab information from the raw form information.
        # Note that we make use of both UserForm and UserProfileForm.
        user_form = UserCreateForm(data=request.POST)
        ##################################################profile_form = userForm(data=request.POST)

        # If the two forms are valid...
        if user_form.is_valid():
            # Save the user's form data to the database.
            user = user_form.save()

            # Update our variable to tell the template registration was successful.
            registered = True

            if request.POST.get("trainer"):
                #redirect to trainer form
                return provide_trainer_info(request, user=user, register=True)
                
            else:
                #redirect to client form
                return provide_client_info(request, user=user, register=True)
                
        # Invalid form or forms - mistakes or something else?
        # Print problems to the terminal.
        # They'll also be shown to the user.
        else:
            print user_form.errors

    # Not a HTTP POST, so we render our form using two ModelForm instances.
    # These forms will be blank, ready for user input.
    else:
        user_form = UserCreateForm
        ##################################################profile_form = userForm()

    # Render the template depending on the context.
    return render_to_response(
            'workout_tracker/register.html',
            {'user_form': user_form,  'registered': registered},
            context)                       


def view_clients(request):
    all_friends = Friend.objects.friends(request.user)
    return render(request, 'friends.html', {'all_friends': all_friends})


def view_pending(request):
    unrejects = Friend.objects.unrejected_requests(user=request.user)
    return render(request, 'pending_follow_requests.html', {'unrejects': unrejects})


def create_follow_request(request):
    other_user = User.objects.get(pk=1)
    new_relationship = Friend.objects.add_friend(request.user, other_user)

    # Can optionally save a message when creating friend requests
    message_relationship = Friend.objects.add_friend(
        from_user=request.user,
        to_user=some_other_user,
        message='Hi, I would like to be your friend',
    )


def accept(request, pid):
    FriendshipRequest.objects.get(id=pid).accept()
    return HttpResponse('friend accepted')


def reject(request, pid):
    FriendshipRequest.objects.get(id=pid).reject()
    return HttpResponse('friend rejected')


def search(request):
  if request.GET:
    query=request.GET['query']
    result = Trainer.objects.none()
    for q in query.split(' '):
      result |= Trainer.objects.filter(user__name__icontains=q)

  return HttpResponse([r.user.username for r in result])


def show(request):
    if not User.objects.all():
        first_user = User.objects.create_superuser('Noha','noha-gomaa@gmail.com','pass')
        first_user.save()
        sec_user = User.objects.create_user('Soad','noha-g@gmail.com','pass')
        sec_user.save()
        new_relationship = Friend.objects.add_friend(first_user, sec_user)
        new_relationship.accept()

    first_user = User.objects.get(pk=1)

    return render_to_response('friends.html', {"user":first_user}, context_instance=RequestContext(request))


def index(request):
    return render(request, 'workout_tracker/index.html')


def homepage(request):
    return render(request,'Homepage.html')


def data(request):
    User.objects.all().delete()

    user = User.objects.create_superuser(
        'admin',
        'alexan.nader@gmail.com', 'pass')
    user.first_name = 'Nader'
    user.last_name = 'Alexan'
    user.save()
    trainer = Trainer(
        user=user,
        date_of_birth='1994-1-1',
        gender='Male',
        type='trainer',
        phone='01005577997',
        experience='so much experience, so much wow',
        education='Saint Fatima el Sele7dar High School'
        )
    trainer.save()
    
    user = User.objects.create_superuser('mirna',
        'mirna@gmail.com', 'pass')
    user.first_name = 'Mirna'
    user.last_name = 'Benjamin'
    user.save()
    client = Client(
        user=user,
        date_of_birth='1994-1-1',
        gender='Female',
        type='client',
        health_issues='All work best, very very awesome, quite tiny',
        weight=40.0,
        height=120.0,
        )
    client.save()
    return trainers(request)

def schedule(request):
    client_workout = request.user.user_info.client.workout.all()
    return render(request,'schedule.html', {'client_workout': client_workout})

def add_workout(request):
     # Like before, get the request's context.
    context = RequestContext(request)

    # If it's a HTTP POST, we're interested in processing form data.
    if request.method == 'POST':
        # Attempt to grab information from the raw form information.
        workout_form = WorkoutForm(data=request.POST)

        # If the two forms are valid...
        if workout_form.is_valid():

            # Save the user's form data to the database.
            user = workout_form.save(commit=False)
            user.posted_by = request.user
            user.save()
            return render_to_response('add_workout.html', {'workout_form': workout_form}, context)

        # Invalid form or forms - mistakes or something else?
        # Print problems to the terminal.
        # They'll also be shown to the user.
        else:
            print workout_form.errors

    # Not a HTTP POST, so we render our form using two ModelForm instances.
    # These forms will be blank, ready for user input.
    else:
        workout_form = WorkoutForm()

    # Render the template depending on the context.
    return render_to_response('add_workout.html',{'workout_form': workout_form},context)               
def password_reset(request, is_admin_site=False,
                   template_name='registration/password_reset_form.html',
                   email_template_name='registration/password_reset_email.html',
                   subject_template_name='registration/password_reset_subject.txt',
                   password_reset_form=PasswordResetForm,
                   token_generator=default_token_generator,
                   post_reset_redirect=None,
                   from_email=None,
                   current_app=None,
                   extra_context=None,
                   html_email_template_name=None):
    if post_reset_redirect is None:
        post_reset_redirect = reverse('password_reset_done')
    else:
        post_reset_redirect = resolve_url(post_reset_redirect)
    if request.method == "POST":
        form = password_reset_form(request.POST)
        if form.is_valid():
            opts = {
                'use_https': request.is_secure(),
                'token_generator': token_generator,
                'from_email': from_email,
                'email_template_name': email_template_name,
                'subject_template_name': subject_template_name,
                'request': request,
                'html_email_template_name': html_email_template_name,
            }
            if is_admin_site:
                warnings.warn(
                    "The is_admin_site argument to "
                    "django.contrib.auth.views.password_reset() is deprecated "
                    "and will be removed in Django 2.0.",
                    RemovedInDjango20Warning, 3
                )
                opts = dict(opts, domain_override=request.get_host())
            form.save(**opts)
            return HttpResponseRedirect(post_reset_redirect)
    else:
        form = password_reset_form()
    context = {
        'form': form,
        'title': _('Password reset'),
    }
    if extra_context is not None:
        context.update(extra_context)

    if current_app is not None:
        request.current_app = current_app

    return TemplateResponse(request, template_name, context)


def password_reset_done(request,
                        template_name='registration/password_reset_done.html',
                        current_app=None, extra_context=None):
    context = {
        'title': _('Password reset sent'),
    }
    if extra_context is not None:
        context.update(extra_context)

    if current_app is not None:
        request.current_app = current_app

    return TemplateResponse(request, template_name, context)


# Doesn't need csrf_protect since no-one can guess the URL
@sensitive_post_parameters()
@never_cache
def password_reset_confirm(request, uidb64=None, token=None,
                           template_name='registration/password_reset_confirm.html',
                           token_generator=default_token_generator,
                           set_password_form=SetPasswordForm,
                           post_reset_redirect=None,
                           current_app=None, extra_context=None):
    """
    View that checks the hash in a password reset link and presents a
    form for entering a new password.
    """
    UserModel = get_user_model()
    assert uidb64 is not None and token is not None  # checked by URLconf
    if post_reset_redirect is None:
        post_reset_redirect = reverse('password_reset_complete')
    else:
        post_reset_redirect = resolve_url(post_reset_redirect)
    try:
        # urlsafe_base64_decode() decodes to bytestring on Python 3
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = UserModel._default_manager.get(pk=uid)
    except (TypeError, ValueError, OverflowError, UserModel.DoesNotExist):
        user = None

    if user is not None and token_generator.check_token(user, token):
        validlink = True
        title = _('Enter new password')
        if request.method == 'POST':
            form = set_password_form(user, request.POST)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect(post_reset_redirect)
        else:
            form = set_password_form(user)
    else:
        validlink = False
        form = None
        title = _('Password reset unsuccessful')
    context = {
        'form': form,
        'title': title,
        'validlink': validlink,
    }
    if extra_context is not None:
        context.update(extra_context)

    if current_app is not None:
        request.current_app = current_app

    return TemplateResponse(request, template_name, context)


def password_reset_complete(request,
                            template_name='registration/password_reset_complete.html',
                            current_app=None, extra_context=None):
    context = {
        'login_url': resolve_url(settings.LOGIN_URL),
        'title': _('Password reset complete'),
    }
    if extra_context is not None:
        context.update(extra_context)

    if current_app is not None:
        request.current_app = current_app

    return TemplateResponse(request, template_name, context)


@sensitive_post_parameters()
@csrf_protect
@login_required
def password_change(request,
                    template_name='registration/password_change_form.html',
                    post_change_redirect=None,
                    password_change_form=PasswordChangeForm,
                    current_app=None, extra_context=None):
    if post_change_redirect is None:
        post_change_redirect = reverse('password_change_done')
    else:
        post_change_redirect = resolve_url(post_change_redirect)
    if request.method == "POST":
        form = password_change_form(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            # Updating the password logs out all other sessions for the user
            # except the current one if
            # django.contrib.auth.middleware.SessionAuthenticationMiddleware
            # is enabled.
            update_session_auth_hash(request, form.user)
            return HttpResponseRedirect(post_change_redirect)
    else:
        form = password_change_form(user=request.user)
    context = {
        'form': form,
        'title': _('Password change'),
    }
    if extra_context is not None:
        context.update(extra_context)

    if current_app is not None:
        request.current_app = current_app

    return TemplateResponse(request, template_name, context)


@login_required
def password_change_done(request,
                         template_name='registration/password_change_done.html',
                         current_app=None, extra_context=None):
    context = {
        'title': _('Password change successful'),
    }
    if extra_context is not None:
        context.update(extra_context)

    if current_app is not None:
        request.current_app = current_app

    return TemplateResponse(request, template_name, context)
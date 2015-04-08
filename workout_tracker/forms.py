from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from workout_tracker.models import Trainer, Client, UserInfo, Workout, Comment

class TrainerUserForm(forms.ModelForm):
	class Meta:
		model = Trainer
		exclude = ['user', 'type']

class ClientUserForm(forms.ModelForm):
	class Meta:
		model = Client
		exclude = ['user', 'type', 'trainer']


class UserCreateForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(UserCreateForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user  

class WorkoutForm(forms.ModelForm):
    class Meta:
        model = Workout
        fields = ("workout", "due_date")






    



 
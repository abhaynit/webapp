from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import recrd
from django.forms import ModelForm

class SignUpForm(UserCreationForm):
    class Meta: 
        model = User
        fields = ['username','first_name','last_name']
        labels = {'username' : 'Registration_no','first_name':'Full_name','last_name':'Branch'}

class student_out_form(ModelForm):
    class Meta:
        model = recrd
        fields = ['purpose','destination']
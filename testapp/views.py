from django.shortcuts import redirect, render,HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm,PasswordChangeForm,SetPasswordForm,UserChangeForm
from .forms import SignUpForm,EditUserProfileForm,EditAdminProfile
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout, update_session_auth_hash
from django.contrib.auth.models import Group, User



# Create your views here.
# this is the simple registration form

def register(request):
    if request.method == "POST":
        ab =  UserCreationForm(request.POST)
        if ab.is_valid():
            ab.save()
    else:
        ab = UserCreationForm()
    return render(request,'signup.html',{'form':ab})

# simple registration form gets completed


# this is customized registration form
def advance_register(request):
    if request.method == "POST":
        ab = SignUpForm(request.POST)
        if ab.is_valid():
            messages.success(request,'CONGRATULATIONS YOUR ACCOUNT HAS BEEN SUCCCEFULLY CREATED ')
            abc = ab.save()
            group = Group.objects.get(name = 'clg')
            abc.groups.add(group)
    else:
        ab = SignUpForm() 
    return  render(request,'signup.html',{'form':ab})

# customize registration form gets completed


# login

def user_login(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/profile/')
    if request.method == "POST":
        fm = AuthenticationForm(request=request ,data = request.POST)
        if fm.is_valid():
            uname = fm.cleaned_data['username']
            upass = fm.cleaned_data['password']
            user = authenticate(username = uname, password =upass )
            if user is not None:
                login(request,user)
                #MORE THAN ONE MESSAGE CAN BE SENT USING THE MESSAGE FRAMEWORK
                #messages.success(request, 'hello from the messsae')
                messages.success(request , 'Logged in successfully !!')
                return HttpResponseRedirect('/profile/')
        else:
            messages.success(request,'please enter the valid credental !!')
    else:
        fm = AuthenticationForm()
    return render(request,'login.html',{'form':fm})

#login completed

# logout

def user_logout(request):
    if request.user.is_authenticated:
        logout(request)
        return HttpResponseRedirect('/login/')
    else:
        messages.success(request,'First login the page !!')
        return HttpResponseRedirect('/login/')

# logout completed

def user_profile(request):
    if request.user.is_authenticated:
        return render(request,'profile.html',{'name':request.user})
    else:
        return HttpResponseRedirect('/login/')


#user password change if the password is konwn in the advance 
def user_change_password(request):
    if not request.user.is_authenticated :
        return HttpResponseRedirect('/login/')
    if request.method == "POST":
        fm = PasswordChangeForm(user = request.user,data = request.POST)
        if fm.is_valid():
            fm.save()
            # in order to be on the page of our choice we have to use other it will redirect to login page automatically
            update_session_auth_hash(request,fm.user)
            return HttpResponseRedirect('/profile/')
    else:
        fm = PasswordChangeForm(user = request.user)
    return render(request,'change_password.html',{'form':fm})

# user_password change completed


#password change when the password not konwn
def forgot_password(request):
    if request.method == "POST":
        fm = SetPasswordForm(user = request.user,data = request.POST)
        if fm.is_valid():
            fm.save()
            # in order to be on the page of our choice we have to use 
            update_session_auth_hash(request,fm.user)
            return HttpResponseRedirect('/profile/')
    else:
        fm = SetPasswordForm(user = request.user)
    return render(request,'change_password.html',{'form':fm})
# password change finished

# user change form started
def user_profile(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            if request.user.is_superuser == True:
                fm = EditAdminProfile(request.POST,instance = request.user)
                users = User.objects.all()
            else:
                fm = EditUserProfileForm(request.POST,instance= request.user)
                users = None
            if fm.is_valid():
                fm.save()
                messages.success(request,'Updated successfully !!')
        #fm = UserChangeForm(instance = request.user)
        # this is customised form
        else:
            if request.user.is_superuser == True:
                users = User.objects.all()
                fm = EditAdminProfile(instance = request.user)
            else:
                users = None
                fm = EditUserProfileForm(instance = request.user)
        return render(request,'profile.html',{'name':request.user,'form':fm,'users':users})
    else:
        return HttpResponseRedirect('/login/')

def user_detail(request,id):
    if request.user.is_authenticated:
        pi = User.objects.get(pk=id)
        if request.method =="POST":
            fm = EditUserProfileForm(request.POST,instance = pi)
            if fm.is_valid():
                fm.save()
                return HttpResponseRedirect('/profile_update/')
        else:      
            fm = EditUserProfileForm(instance = pi)
        return  render(request,'userdetail.html',{'form':fm})
    else:
        return HttpResponseRedirect('/login/')

def user_dashboard(request):
    if request.user.is_authenticated:
        return render (request,'dashboard.html',{'name':request.user.username})
    else:
        return HttpResponseRedirect('/login/')


def test(request):
    if request.method == "POST":
        ab =  UserCreationForm(request.POST)
        if ab.is_valid():
            ab.save()
    else:
        ab = UserCreationForm()
    return render(request,'hello.html',{'form':ab})



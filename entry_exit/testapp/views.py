from django.shortcuts import render,HttpResponseRedirect
from .forms import SignUpForm,student_out_form
from django.contrib.auth import authenticate,login,logout, update_session_auth_hash
from django.contrib.auth.forms import AuthenticationForm,PasswordChangeForm
from django.contrib import messages
from .models import recrd
import datetime
def register(request):
    if request.user.is_superuser:
        if request.method == "POST":
            sign_up_form = SignUpForm(request.POST)
            if sign_up_form.is_valid():
                sign_up_form.save()
                return HttpResponseRedirect('/')
            else:
                messages.success(request,"A USER ALREADY EXIST WITH USER NAME")
                return HttpResponseRedirect('/login/')

        else:
            sign_up_form = SignUpForm() 
            return  render(request,'register.html',{'form':sign_up_form})
    else:
        messages.success(request,"YOU ARE NOT AUTHORISED TO USE THIS PAGE")
        return HttpResponseRedirect('/')

def user_login(request):
    if request.user.is_authenticated:
       return HttpResponseRedirect('/dashboard/')
    if request.method == "POST":
        fm = AuthenticationForm(request=request ,data = request.POST)
        if fm.is_valid():
            uname = fm.cleaned_data['username']
            upass = fm.cleaned_data['password']
            print(uname,upass)
            user = authenticate(username = uname, password =upass )
            if user is not None:
                login(request,user)
                return HttpResponseRedirect('/dashboard/')
        else:
            messages.success(request,'you are not a valid user')
    else:
        fm = AuthenticationForm()
    return render(request,'login.html',{'form':fm,'nam':'LOGIN'})

def user_logout(request):
    if request.user.is_authenticated:
        logout(request)
        return HttpResponseRedirect('/')
    else:
        messages.success(request,'First login the page !!')
        return HttpResponseRedirect('/')

    
def student_out(request):
    duplicate  = recrd.objects.all().filter(student_id = request.user.username,entry_time = None)
    if duplicate:
        messages.success(request,'A PASS HAS BEEN ALREADY ISSUED WITH YOUR ID YOU CAN NOT APPLY FOR TWO PASS AT A TIME')
        return HttpResponseRedirect('/dashboard/')
    if request.method == 'POST':
        ab = student_out_form(request.POST)
        if ab.is_valid():
            purpose = ab.cleaned_data['purpose']
            destination = ab.cleaned_data['destination']
            #branch = ab.cleaned_data['student_branch']
            ab = recrd(student_id = request.user.username ,student_name = request.user.get_short_name(),student_branch = request.user.last_name,purpose= purpose,destination = destination)
            ab.save()
            return HttpResponseRedirect('/dashboard/')

    else:
        fm = student_out_form()
        return render (request,'student_out.html',{'form':fm,'nam':'EXIT_FORM'})

def already_issued_pass(request):
    if request.user.is_authenticated:
        data = recrd.objects.all().filter(student_id = request.user.username,entry_time = None)
        return render(request,'dashboard.html',{'form':data})
def dashboard(request):
    exit_data = recrd.objects.all().filter(entry_time = None).order_by('student_id') 
    if request.method == 'POST':
        ab = request.POST['sear']
        data = recrd.objects.all().filter(student_id = ab,entry_time = None)
        if data:
            return render(request,'dashboard.html',{'student_detail':data,'reg':data[0].student_id,'exit_data_student':exit_data})
        else:
            messages.success(request,'NO ANY PASS HAS BEEN ISSUED FOR THE GIVEN REGISTRATION NO ')
            return render(request,'dashboard.html',{'exit_data_student':exit_data})
    else:
        if not request.user.is_staff:
            qw = recrd.objects.all().filter(student_id = request.user.username).order_by('-exit_time')
            return render (request,'dashboard.html',{'form':qw,'show':1})
        else:
            #exit_data = recrd.objects.all().filter(entry_time = None) 
            return render(request,'dashboard.html',{'exit_data_student':exit_data})

def guard_submit(request,id):
    ab = recrd.objects.get(student_id = int(id),entry_time = None)
    ab.entry_time = datetime.datetime.now()
    ab.save()
    return HttpResponseRedirect('/dashboard/')

def user_change_password(request):
    if not request.user.is_authenticated :
        return HttpResponseRedirect('/')
    if request.method == "POST":
        fm = PasswordChangeForm(user = request.user,data = request.POST)
        if fm.is_valid():
            fm.save()
            # in order to be on the page of our choice we have to use 
            #  update_session_auth_hash otherwise 
            #  it will redirect to login page automatically
            update_session_auth_hash(request,fm.user)
            return HttpResponseRedirect('/dashboard/')
    else:
        fm = PasswordChangeForm(user = request.user)
    return render(request,'change_password.html',{'form':fm,'nam':'CHANGE PASSWORD'})
    
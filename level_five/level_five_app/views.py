from django.shortcuts import render
from level_five_app.forms import UserForm,userinfoform

from django.contrib.auth import authenticate,logout,login
from django.http import HttpResponse,HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required


def index(request):
    return render(request,'level_five_app/index.html')

@login_required()
def special(request):
    return HttpResponse("You are logged In!!")

@login_required()
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

def register(request):
    registered = False
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = userinfoform(data=request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            if 'profile_image' in request.FILES:
                profile.profile_image = request.FILES['profile_image']
                # print("helllo")
            profile.save()

            registered = True
        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = userinfoform()
    return render(request,'level_five_app/registaration.html',{'user_form':user_form,'profile_form':profile_form,'registered':registered})


def user_login(request):
    if request.method =='POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user=authenticate(username=username,password=password)

        if user:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(reverse('index'))
            else:
                print("user is not Active")
        else:
            print("someone tried to logged in but get failed")
            print("username:{},password:{}".format(username,password))
            return HttpResponse("Invalid Login")
    else:
        return render(request,'level_five_app/login.html')


# Create your views here.

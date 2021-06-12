from datetime import date
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from .models import Candidate, Position, Registration,ControlVote
# Create your views here.

# This view is for HomePage view that show the normal home page view
def home(request):
    return render(request, 'poll/home.html')

def register(request):
    if request.method == "POST":
        # Get the post parameters
        username = request.POST['username']
        email = request.POST['email']
        First_name = request.POST['First_name']
        Last_name = request.POST['Last_name']
        dob = request.POST['dob']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        # check for errorneous input
        dat = dob.split("-", 2)
        yy = int(dat[0])
        dd = int(dat[1])
        mm = int(dat[2])
        date_of_birth = date(yy, dd, mm)
        present = date.today()
        age = present.year - date_of_birth.year - ((present.month, present.day) < (date_of_birth.month, date_of_birth.day))
        if age<18:
            messages.error(request,"Sorry you are not eligible for voting because you are under 18.")
            return redirect('home')
        if User.objects.filter(username=username).exists():
            messages.error(request, 'This Aadhaar is Already Used')
            return redirect('home')
        if User.objects.filter(email=email).exists():
            messages.error(request, 'This Email is already Used')
            return redirect('home')
        if (pass1 != pass2):
            messages.error(request, " Passwords do not match")
            return redirect('home')

        # Create the user
        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name = First_name
        myuser.last_name = Last_name
        myuser.save()
        extendedregister = Registration(user=myuser, First_name=First_name, Last_name=Last_name,dob=dob)
        extendedregister.save()
        messages.success(request, "You are successfully registered")
        return redirect('home')

    else:
        return HttpResponse("404 - Not found")


def view_login(request):
    if request.method == "POST":
        # Get the post parameters
        loginusername = request.POST['loginusername']
        loginpassword = request.POST['loginpassword']

        user = authenticate(username=loginusername, password=loginpassword)
        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            messages.error(request, "Invalid credentials! Please try again")
            return redirect("home")

    return HttpResponse("404- Not found")


@login_required()
def position_view(request):
    obj = Position.objects.all()
    return render(request, 'poll/positions.html', {'obj': obj})

@login_required()
def candidate_view(request, pos):
    obj = get_object_or_404(Position, pk=pos)
    if request.method == "POST":
        temp = ControlVote.objects.get_or_create(user=request.user, position=obj)[0]
        print(temp)
        if temp.status == False:
            temp2 = Candidate.objects.get(pk=request.POST.get(obj.title))
            temp2.total_vote += 1
            temp2.save()
            temp.status = True
            temp.save()
            messages.success(request, "Congrats! you VOTED Successfully.")
            return redirect('home')
        else:
            messages.error(request, "Opps! You have already voted for this position")
            return redirect('home')

    else:
        return render(request, 'poll/candidate.html', {'obj': obj})

@login_required()
def result(request):
    vote = Candidate.objects.all()
    return render(request, 'poll/result.html', {'vote': vote})

@login_required
def view_logout(request):
    logout(request)
    messages.success(request, "You are successfully logged out")
    return redirect('home')

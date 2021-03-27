from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.urls import reverse
from django import forms
from django.contrib.auth.decorators import login_required

def welcome(request):
    return render(request, "notetaking/welcome.html")

@login_required
def index(request):
    return render(request, "notetaking/index.html", {
        "classes": None
    })

def login_view(request):
    if request.method == "POST":
        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "notetaking/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "notetaking/login.html")


def logout_view(request):
    return HttpResponse("TODO")

def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")



@login_required
def class_view(request, class_id):
    return HttpResponse("TODO")


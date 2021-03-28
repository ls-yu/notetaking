from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.urls import reverse
from django import forms
from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from .models import User, UserProfile, Class, Note
from django.db import IntegrityError
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import get_object_or_404
from django.utils.crypto import get_random_string
from django.utils.safestring import mark_safe



class ClassForm(forms.ModelForm):
    class Meta:
        model = Class
        fields = ['name']

class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['title', 'text']
        widgets = {
            'title': forms.TextInput(attrs={
            'class': 'form-item'
            }),
            'text': forms.Textarea(attrs={
            'rows': 20,
            'class': 'form-item'
            })
         }
        labels = {
            "title": mark_safe('Title <br>'),
            "text": mark_safe('Text <br>')
        }

def welcome(request):
    return render(request, "notetaking/welcome.html")


@login_required
def index(request):
    userprofile = get_object_or_404(UserProfile, pk=request.user)
    classes = None
    if userprofile.is_teacher:
        classes = Class.objects.filter(teacher=userprofile)
    else:
        classes = Class.objects.filter(students=userprofile)
    return render(request, "notetaking/index.html", {
        "userprofile": userprofile,
        "classes": classes,
        "is_teacher": userprofile.is_teacher,
        "userprofile": userprofile
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
    logout(request)
    return render(request, "notetaking/welcome.html")

def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        category = request.POST["category"]
        is_teacher = False
        is_notetaker = False 
        is_noterequester = False
        if category == "teacher":
            is_teacher = True
            is_notetaker = False
            is_noterequester = False
        elif category == "notetaker":
            is_teacher = False
            is_notetaker = True
            is_noterequester = False
        elif category == "noterequester":
            is_teacher = False
            is_notetaker = False
            is_noterequester = True
        else:
            return render(request, "notetaking/register.html", {
                "message": "Select a user type."
            })
        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "notetaking/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
            userProfile = UserProfile(user=user, is_teacher=is_teacher, is_notetaker=is_notetaker, is_noterequester=is_noterequester)
            userProfile.save()
            print(userProfile.is_teacher)
        except IntegrityError:
            return render(request, "notetaking/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "notetaking/register.html")

@login_required
def new_class(request):
    if request.method == "POST":
        userprofile = get_object_or_404(UserProfile, pk=request.user)
        form = ClassForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data["name"]
            code = get_random_string(length=6, allowed_chars='1234567890ABCDEFGHIJKLMNOPQRSTUVWXYZ')
            code_list = Class.objects.all().values_list('class_code')
            while (code in code_list):
                code = get_random_string(length=6, allowed_chars='1234567890ABCDEFGHIJKLMNOPQRSTUVWXYZ')
            new_class = Class(name=name, class_code=code, teacher=userprofile)
            new_class.save()
            return HttpResponseRedirect(reverse("index"))
        else:
            return HttpResponse("Failed to create new class.")
    else:
        form = ClassForm()
        return render(request, "notetaking/new_class.html", {
            "form": form
        })


@login_required
def class_view(request, class_code):
    if request.method == "POST":
        form = NoteForm(request.POST)
        if form.is_valid():
            the_class = get_object_or_404(Class, class_code=class_code)
            title = form.cleaned_data["title"]
            text = form.cleaned_data["text"]
            date = datetime.now().strftime("%x")
            notetaker = get_object_or_404(UserProfile, pk=request.user)
            note = Note(which_class=the_class,title=title, text=text, notetaker=notetaker, date=date)
            note.save()
        else:
            return HttpResponse("Failed to submit note")
        return HttpResponseRedirect(reverse("class_view", args=[class_code]))
    else:
        form = NoteForm()
        the_class = get_object_or_404(Class, class_code=class_code)
        notes = Note.objects.filter(which_class=the_class)
        userprofile = get_object_or_404(UserProfile, user=request.user)
        return render(request, "notetaking/class_view.html", {
            'class': the_class,
            'form': form,
            'notes': notes,
            'userprofile':userprofile
        })

def note(request, note_id):
    note = get_object_or_404(Note, note_id=note_id)
    return render(request, "notetaking/note.html", {
        'note': note
    })

def join_class(request):
    if request.method == 'POST':
        code = request.POST["code"]
        joined_class = get_object_or_404(Class, class_code=code)
        userprofile = get_object_or_404(UserProfile, pk=request.user)
        joined_class.students.add(userprofile)
        joined_class.save()
        return HttpResponseRedirect(reverse(index))
    else:
        return render(request, "notetaking/join_class.html")
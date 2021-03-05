from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.forms import inlineformset_factory
# Create your views here.
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group

from django.contrib import messages

from .models import *
from .forms import CreateUserForm

from .decorators import unauthenticated_user, allowed_users, admin_only


@login_required(login_url='login')
def home(request):
    return render(request, 'movies/home.html')

@login_required(login_url='login')
def search(request):
    return render(request, 'movies/search.html')


@login_required(login_url='login')
def movie(request, pk):
    movies = Movie.objects.all()
    movie_name = Movie.objects.get(id=pk)
    movie_pic = movie_name.picture
    context = {'movies':movies, 'movie_name':movie_name, 'pic':movie_pic, 'id':pk}
    return render(request, 'movies/movie.html', context)


@unauthenticated_user
def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username,password=password)

        if user is not None:
            login(request, user)
            return redirect('home')

        else:
            messages.info(request, 'Username or Password is Incorrect')
            return render(request, 'movies/login.html')

    context = {}
    return render(request, 'movies/login.html', context)


def logoutUser(request):
    logout(request)
    return redirect('login')


@unauthenticated_user
def registerPage(request):

    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            group = Group.objects.get(name='customer')
            user.groups.add(group)
            Customer.objects.create(
                user=user,
                )
            messages.success(request, 'Congratulations! ' + username)
            return redirect('login')

    context = {'form':form}
    return render(request, 'movies/register.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def userPage(request):
    context = {}
    return render(request, 'movies/user.html')


#@login_required(login_url='login')
#@allowed_users(allowed_roles=['admin'])
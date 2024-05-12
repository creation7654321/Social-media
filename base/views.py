from django.shortcuts import render, redirect
from . models import Post
from . forms import PostForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Q

# Create your views here.
def home(request):
    
    # posts = Post.objects.all()
    q = request.GET.get('q') if request.GET.get('q') != None else ''


    posts = Post.objects.filter( Q(user__username__icontains =q) |
                                Q(title__icontains = q)
                                )
    context = {'posts': posts}
    return render(request, 'home.html', context)


def postdetails(request, pk):
    postdetails = Post.objects.get(id=pk)
    context ={'postdetails':postdetails}
    return render(request, 'postdetails.html', context)

@login_required(login_url='login')
def createPost(request):
    form = PostForm()

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid:
            form.save()
            return redirect('home')



    context ={'form': form}
    return render(request, 'post_form.html', context)

@login_required(login_url='login')
def updatePost(request, pk):
    postdetails = Post.objects.get(id=pk)
    form = PostForm(instance=postdetails)


    if request.method =='POST':
        form = PostForm(request.POST, request.FILES, instance=postdetails)
        if form.is_valid:
            form.save()
            return redirect('home')
        
    context={'form': form}
    return render(request, 'post_form.html', context)

    
@login_required(login_url='login')
def deletePost(request, pk):
    post= Post.objects.get(id=pk)
    context = {'obj': post}

    if request.method == 'POST' :
        post.delete()
        return redirect('home')
    

    return render(request, 'delete.html', context)

    
def loginPage(request):

    page= 'login'

    if request.user.is_authenticated:
        return redirect('home')
    

    if request.method=='POST':
        username= request.POST.get('username')
        password= request.POST.get('password')

        try:
            user = User.objects.get(username=username)

        except:
            messages.error(request, 'User doesnot exist')

        user = authenticate(request, username=username, password= password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username or password doesnot exist')

    context ={'page':page}
    return render(request, 'login_register.html', context)


def logoutUser(request):
    logout(request)
    return redirect('home')

def registerPage(request):
    form = UserCreationForm()

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
    else:
        messages.error(request, 'An error occured during registration')

    return render(request, 'login_register.html',{'form':form})


def profilePage(request, pk):
    
    user = User.objects.get(id=pk)
    posts = user.post_set.all()
    context = {'posts': posts, 'user':user}
    return render(request, 'profile.html', context)


from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.decorators import login_required

from .forms import PostForm, RegisterForm, LoginForm
from .models import User, Post, Comment, Service, Skill, Image

# Create your views here.


def home(request):
    if request.method == "GET":
        posts = Post.objects.all()
        context = {"posts": posts}
        return render(request, "home/homepage.html", context)


def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            # messages.success(request,f"User {form.cleaned_data['username']} created successfully!")
            return redirect("home-page")
        return render(request, "accounts/register.html", {"form": form})
    return render(request, "accounts/register.html")


def signin(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(username=username, password=password)
            if user is not None:
                login(
                    request, user, backend="django.contrib.auth.backends.ModelBackend"
                )
                posts = Post.objects.all()
                context = {"posts": posts, "user": user}
                try:
                    return render(request, context)
                except:
                    return render(request, "home/homepage.html", context)
            else:
                messages.error(request, "Wrong username or password!")
                return render(request, "accounts/login.html")

    return render(request, "accounts/login.html")


def signout(request):
    logout(request)
    return redirect("home-page")


@login_required(login_url="signin")
def profile(request):
    usr = request.user
    if request.method == "POST":
        data = request.POST
        usr.first_name = data["first_name"]
        usr.last_name = data["last_name"]
        if data["username"] != usr.username:
            if not User.objects.filter(username=data["username"]).exists():
                usr.username = data["username"]
            else:
                messages.error(request, "Username already exists!")
                return redirect("profile")

        if data["email"] != usr.email:
            if not User.objects.filter(email=data["email"]).exists():
                usr.email = data["email"]
                messages.success(request, "Email updated successfully!")
            else:
                messages.error(request, "Email already exists!")
                return redirect("profile")
        if data["password"] != data["confirm_password"]:
            messages.error(request, "Passwords do not match!")
            return redirect("profile")
        else:
            usr.set_password(data["password"])
            messages.success(request, "Password changed successfully!")

        if data["skills"]:
            skls = data["skills"].split(",")
            for sk in skls:
                sk = sk.strip(" ").capitalize()
                if not Skill.objects.filter(skill=sk).exists():
                    new_skill = Skill.objects.create(skill=sk)
                    usr.skills.add(new_skill)
                else:
                    usr.skills.add(Skill.objects.get(skill=sk))

        usr.save()
        return redirect("profile")
    form = RegisterForm(instance=usr)
    return render(request, "accounts/profile.html", {"form": form, "user": usr})


def update_profile_pic(request):
    if request.method == "POST":
        try:
            usr = request.user
            usr.image = request.FILES["image"]
            usr.save()
        except:
            return redirect("profile")
    return redirect("profile")


def view_post(request, id=None):
    try:
        post = Post.objects.get(id=id)
        comments = post.comment_set.all()
        return render(request, "home/post.html", {"post": post, "comments": comments})
    except Post.DoesNotExist:
        return HttpResponse("Post doesnot exist!!")
    except Exception as e:
        print(e)
        return HttpResponse("Something went wrong!!")


@login_required(login_url="signin")
def add_post(request):
    form = PostForm()
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            form.save(request.user)
            return redirect("home-page")
        print(form.errors)
        return render(request, "home/addpost.html")
    return render(request, "home/addpost.html")


@login_required(login_url="signin")
def delete_post(request, id=None):
    try:
        post = Post.objects.get(id=id)
        post.delete()
        # messages.success(request, "Post deleted successfully!")
    except Exception as e:
        print(e)
        # messages.error(request, "Post couldnot be deleted!")
    return redirect("home-page")


@login_required(login_url="signin")
def add_comment(request, id=None):
    if request.method == "POST":
        try:
            content = request.POST.get("comment-content")
            post = Post.objects.get(id=id)
            Comment.objects.create(author=request.user, content=content, post=post)
            post.commentCount += 1
            post.save()
        except Exception as e:
            return HttpResponse(e)
    return HttpResponseRedirect(reverse("view-post", args=[id]))


def services(request):
    services = Service.objects.all()
    return render(
        request, "services/services.html", {"services": services, "user": request.user}
    )


def delete_service(request, id=None):
    try:
        service = Service.objects.get(id=id)
        service.delete()
        # messages.success(request, "Service deleted successfully!")
    except Exception as e:
        print(e)
        # messages.error(request, "Service couldnot be deleted!")
    return redirect("services")


@login_required(login_url="signin")
def add_service(request):
    if request.method == "POST":
        data = request.POST
        new_service = Service(
            title=data["title"],
            description=data["description"],
            price=data["price"],
            provider=request.user,
        )
        new_service.save()
        sks = data.getlist("skills")
        for sk in sks:
            new_service.skills.add(Skill.objects.get(id=sk))
        # messages.success(request, "Service added successfully!")
    return redirect("services")


@login_required(login_url="signin")
def add_new_skill(request):
    if request.method == "POST":
        data = request.POST
        new_skill = Skill(name=data["name"])
        new_skill.save()
        # messages.success(request, "Skill added successfully!")
    return redirect("profile")


@login_required(login_url="signin")
def assign_skill(request):
    if request.method == "POST":
        data = request.POST
        usr = request.user
        sk = Skill.objects.get(id=data["skill"])
        usr.skills.add(sk)
        # messages.success(request, "Skill assigned successfully!")
    return redirect("profile")

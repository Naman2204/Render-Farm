import subprocess
import os
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import redirect, render

from .models import FileData, Suggestions


# Create your views here.
def base_page_route(request: HttpRequest) -> HttpResponse:
    """[Function]"""

    return render(request, "base/index.html")


def about_page_route(request: HttpRequest) -> HttpResponse:
    """[Function]"""

    return render(request, "base/about.html")


def signin_page_route(request: HttpRequest) -> HttpResponse:
    """[Function]"""

    if request.method != "POST":
        return JsonResponse({"error": {"code": 405, "message": "Method not allowed."}})
    username = request.POST.get("username")
    password = request.POST.get("password")
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user=user)
    return redirect("/")


def suggestions_page_route(request: HttpRequest) -> HttpResponse:
    """[Function]"""

    if request.method != "POST":
        return JsonResponse({"error": {"code": 405, "message": "Method not allowed."}})
    name = request.POST.get("name")
    phone = request.POST.get("number")
    email = request.POST.get("email")
    content = request.POST.get("message")
    obj = Suggestions(name=name, phone=phone, email=email, content=content)
    obj.save()
    messages.info(request, f"{name.title()}, your Suggestion has been Submitted!")
    return redirect("/")

def signup_page_route(request: HttpRequest) -> HttpResponse:
    """[Function]"""

    if request.method == "POST":
        email = request.POST.get("email")
        username = request.POST.get("username")
        password = request.POST.get("password")
        try:
            user = User.objects.create_user(username, email, password)
        except Exception as e:
            pass
        else:
            login(request, user=user)
        return redirect("/")
    return render(request, "base/signup.html")


def logout_page_route(request: HttpRequest) -> HttpResponse:
    """[Function]"""

    logout(request)
    return redirect("/")

def send_mail(request: HttpRequest, path: str) -> None:
    """[Function]"""

    message = EmailMessage(
        "Your file has been rendered.",
        "Thanks for using our RenderFarm rendering service.",
        settings.EMAIL_HOST_USER,
        [request.user.email],
    )
    message.attach_file(path=path)
    message.send()


@login_required(login_url="/")
def upload_page_route(request: HttpRequest) -> HttpResponse:
    """[Function]"""

    if request.method == "POST":
        file = request.FILES.get("file")
        data = FileData(user=request.user, file=file)
        data.save()
        subprocess.call(
            ["blender.exe", "-b", str(data.file), "-o", "//../renders/render", "-F", "PNG", "-f",
             "1"]
        )
        send_mail(request=request, path="renders/render0001.png")
        os.remove("renders/render0001.png")
        messages.info(request, f"{file} file has been rendered and has been sent to your e-mail.")
        return redirect("base")
    return render(request, "base/upload.html")

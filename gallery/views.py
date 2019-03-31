import json

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
from rest_framework.exceptions import ValidationError
from rest_framework_jwt.serializers import VerifyJSONWebTokenSerializer

from .models import Image, ImageForm


# Create your views here.
@csrf_exempt
def index(request):
    images_list = Image.objects.all()
    if request.method == 'POST':
        jsonData = json.loads(request.body)
        data = {'token': jsonData['token']}

        try:
            valid_data=VerifyJSONWebTokenSerializer().validate(data)
        except ValidationError as e:
            pass
        else:
            if valid_data['user']:
                images_list = Image.objects.filter(user=valid_data['user'])
    return HttpResponse(serializers.serialize("json", images_list))


@csrf_exempt
def add_image(request):
    message = 'no'
    if request.method == 'POST':
        jsonData = json.loads(request.body)
        dataToken = {'token': jsonData['token']}

        try:
            valid_data=VerifyJSONWebTokenSerializer().validate(dataToken)
        except ValidationError as e:
            pass
        else:
            if valid_data['user']:
                new_image = Image(
                    name=jsonData['name'],
                    url=jsonData['url'],
                    description=jsonData['description'],
                    type=jsonData['type'],
                    user=valid_data['user']
                )
                new_image.save()
                message='ok'
            else:
                message = 'usuario no válido'
    return JsonResponse({"message": message})




@csrf_exempt
def view_images(request):
    return render(request, "gallery/index.html")


@csrf_exempt
def add_new_image(request):
    return render(request, "gallery/image_form.html")


@csrf_exempt
def add_user_view(request):
    if request.method == 'POST':
        jsonUser = json.loads(request.body)
        username = jsonUser['username']
        first_name = jsonUser['first_name']
        last_name = jsonUser['last_name']
        password = jsonUser['password']
        email = jsonUser['email']

        user_model = User.objects.create_user(username=username, password=password)
        user_model.first_name = first_name
        user_model.last_name = last_name
        user_model.email = email
        user_model.save()
    return HttpResponse(serializers.serialize("json", [user_model]))


@csrf_exempt
def add_user(request):
    return render(request, "gallery/register.html")


@csrf_exempt
def add_user_view(request):
    if request.method == 'POST':
        jsonUser = json.loads(request.body)
        username = jsonUser['username']
        first_name = jsonUser['first_name']
        last_name = jsonUser['last_name']
        password = jsonUser['password']
        email = jsonUser['email']

        user_model = User.objects.create_user(username=username, password=password)
        user_model.first_name = first_name
        user_model.last_name = last_name
        user_model.email = email
        user_model.save()
    return HttpResponse(serializers.serialize("json", [user_model]))


@csrf_exempt
def add_user(request):
    return render(request, "gallery/register.html")


@csrf_exempt
def login_view(request):
    if request.method == 'POST':
        jsonUser = json.loads(request.body)
        username = jsonUser['username']
        password = jsonUser['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            message = "ok"
        else:
            message = 'Nombre de usuario o contraseña incorrectos'

    return JsonResponse({"message": message})


def login_user(request):
    return render(request, "gallery/login.html")


@csrf_exempt
def logout_view(request):
    logout(request)
    return JsonResponse({"message": 'ok'})


@csrf_exempt
def is_logged_view(request):
    if request.user.is_authenticated():
        message = 'ok'
    else:
        message = 'no'

    return JsonResponse({"message": message})



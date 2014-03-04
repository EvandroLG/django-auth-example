import json
from django.shortcuts import render_to_response
from django.core.context_processors import csrf
from django.contrib import auth
from django.http import HttpResponse
from forms import UserRegistrationForm


def create_user_json(user):
  is_post = hasattr(user, 'POST')

  obj_user = {
    'username': user.POST['username'] if is_post else user.username,
    'email':  user.POST['email'] if is_post else user.email
  }

  return json.dumps(obj_user)


def register(request):
  is_post = request.method == 'POST'

  if is_post:
    form = UserRegistrationForm(request.POST)

    if form.is_valid():
      form.save()
      data = create_user_json(request)

      return HttpResponse(data, mimetype='application/json')

    return HttpResponse(status=401)

  args = {}
  args.update(csrf(request))
  args['form'] = UserRegistrationForm()

  return render_to_response('users/register.html', args)


def login(request):
  context = {}
  context.update(csrf(request))

  return render_to_response('users/login.html', context)


def auth_view(request):
  username = request.POST['username']
  password = request.POST['password']
  user = auth.authenticate(username=username, password=password)
  is_valid = user is not None

  if is_valid:
      auth.login(request, user)
      data = create_user_json(user)

      return HttpResponse(data, mimetype='application/json')

  return HttpResponse(status=401)


def logout_view(request):
  auth.logout(request)
  return HttpResponse(status=200)

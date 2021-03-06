from django.shortcuts import render, redirect, HttpResponse
from django.urls import reverse
from django.contrib import messages
import bcrypt

from app.models import User, Message, Comment

# Default route to login or register
def index(request):
  return render(request, 'index.html')

# POST route to login an existing user
def login(request):
  if request.method == 'POST':
    if 'login_err' in request.session:
      del request.session['login_err']
    if not 'login_attempts' in request.session:
      request.session['login_attempts'] = 1
    else:
      request.session['login_attempts'] += 1
    users = User.objects.filter(email=request.POST['email'])
    if users:
      user = users[0]
      if bcrypt.checkpw(request.POST['pw'].encode(), user.pw_hash.encode()):
        request.session['user_id'] = user.id
        request.session['user_name'] = user.first_name
        request.session['token'] = User.objects.gen_token(user.id)
        return redirect(reverse('app:wall'))

    request.session['login_err'] = True
    messages.error(
      request,
      f'Invalid credentials. {request.session["login_attempts"]} bad attempts.'
    )
  return redirect(reverse('app:index'))

# POST route to register a new user
def register(request):
  if request.method == 'POST':
    if 'reg_err' in request.session:
      del request.session['reg_err']
    errors = User.objects.validate(request.POST)
    if len(errors) == 0:
      user = User.objects.create(
        first_name=request.POST['first_name'],
        last_name=request.POST['last_name'],
        email=request.POST['email'],
        pw_hash=bcrypt.hashpw(
          request.POST['pw'].encode(), bcrypt.gensalt()).decode()
      )
      request.session['user_id'] = user.id
      request.session['user_name'] = user.first_name
      request.session['token'] = User.objects.gen_token(user.id)
      return redirect(reverse('app:wall'))

    request.session['reg_err'] = True
    for key, value in errors.items():
      messages.error(request, value)
  return redirect(reverse('app:index'))

# GET route for a logged in user
def wall(request):
  is_auth = User.objects.is_user_authenticated(
    request.session['user_id'],
    request.session['token']
  )
  if is_auth:
    context = {
      'messages': Message.objects.all().order_by('-created_at')
    }
    return render(request, 'wall.html', context)
  return redirect(reverse('app:index'))

# POST route for creating a new message
def create_message(request):
  if request.method == 'POST':
    user_id = request.session['user_id']
    is_auth = User.objects.is_user_authenticated(
      user_id,
      request.session['token']
    )
    if is_auth:
      Message.objects.create(
        owner = User.objects.get(id=user_id),
        text = request.POST['message_text']
      )
  return redirect(reverse('app:wall'))

# POST route for deleting a message for logged in user
def destroy_message(request, message_id):
  if request.method == 'POST':
    user_id = request.session['user_id']
    is_auth = User.objects.is_user_authenticated(
      user_id,
      request.session['token']
    )
    try:
      message = Message.objects.get(id=message_id)
    except Message.DoesNotExist:
      return HttpResponse('Message does not exist', status=404)
    if not is_auth or message.owner.id != user_id:
      return HttpResponse('This is not your message', status=401)

    message.delete()
  return redirect(reverse('app:wall'))

# POST route for creating a new comment on a message
def create_comment(request):
  if request.method == 'POST':
    user_id = request.session['user_id']
    message = Message.objects.get(id=request.POST['message_id'])
    is_auth = User.objects.is_user_authenticated(
      user_id,
      request.session['token']
    )
    if is_auth:
      Comment.objects.create(
        owner = User.objects.get(id=user_id),
        on_message = message,
        text = request.POST['comment_text']
      )
  return redirect(reverse('app:wall'))

# POST route for deleting a comment for logged in user
def destroy_comment(request, comment_id):
  if request.method == 'POST':
    user_id = request.session['user_id']
    is_auth = User.objects.is_user_authenticated(
      user_id,
      request.session['token']
    )
    try:
      comment = Comment.objects.get(id=comment_id)
    except Comment.DoesNotExist:
      return HttpResponse('Comment does not exist', status=404)
    if not is_auth or comment.owner.id != user_id:
      return HttpResponse('This is not your message', status=401)

    comment.delete()
  return redirect(reverse('app:wall'))

# GET route for logging out a user
def logout(request):
  request.session.clear()
  return redirect(reverse('app:index'))

# GET route for checking email availability, sends 'available' or 'unavailable'
def check_email(request, email):
  if len(User.objects.filter(email=email)) == 0:
    return HttpResponse('available')
  return HttpResponse('unavailable')

from django.shortcuts import render, redirect, HttpResponse
from django.urls import reverse

# Default route to login or register
def index(request):
  return render(request, 'index.html')

# POST route to login an existing user
def login(request):
  return redirect(reverse('app:wall'))

# POST route to register a new user
def register(request):
  return redirect(reverse('app:wall'))

# GET route for a logged in user
def wall(request):
  return render(request, 'wall.html')

# POST route for creating a new message
def create_message(request):
  return redirect(reverse('app:wall'))

# POST route for deleting a message for logged in user
def destroy_message(request, message_id):
  return redirect(reverse('app:wall'))

# POST route for creating a new comment on a message
def create_comment(request):
  return redirect(reverse('app:wall'))

# POST route for deleting a comment for logged in user
def destroy_comment(request, comment_id):
  return redirect(reverse('app:wall'))

# GET route for logging out a user
def logout(request):
  request.session.clear()
  return redirect(reverse('app:index'))

# GET route for checking email availability, sends 'available' or 'unavailable'
def check_email(request, email):
  print(email)
  return HttpResponse('hello')

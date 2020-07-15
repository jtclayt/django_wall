from django.shortcuts import render, redirect
from django.urls import reverse


def index(request):
  return render(request, 'index.html')

def login(request):
  return redirect(reverse('app:wall'))

def wall(request):
  return render(request, 'wall.html')

def create_message(request):
  return redirect(reverse('app:wall'))

def destroy_message(request, message_id):
  return redirect(reverse('app:wall'))

def create_comment(request):
  return redirect(reverse('app:wall'))

def destroy_message(request):
  return redirect(reverse('app:wall'))

def logout(request):
  request.session.clear()
  return redirect(reverse('app:index'))

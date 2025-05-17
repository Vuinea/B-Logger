from django.shortcuts import render, redirect
from .forms import RegisterForm

# Create your views here.

def register(request):
  if request.user.is_authenticated:
    return redirect("/posts/")
  if request.method == "POST":
    form = RegisterForm(data=request.POST)
    if form.is_valid():
      form.save()
      return redirect('login')
  else:
    form = RegisterForm()
  return render(request, "registration/register.html", {"form":form})

def main(request):
    return redirect("/posts/")

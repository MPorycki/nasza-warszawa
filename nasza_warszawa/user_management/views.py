from django.shortcuts import render, redirect

from .forms import SignUpForm

# Create your views here.
def register(request):
    print('register')
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.set_password(user.password)
            user.save()

            return redirect('/')
    else:
        form = SignUpForm()

def logout(request):
   return 'logout'
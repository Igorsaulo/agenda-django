from django.contrib import messages, auth
from contact.forms import CustomUserCreationForm, UserUpdateForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from django.urls import reverse

def register(request):
    form_action = reverse('contact:register')
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Usuario criado com sucesso!')
            return redirect('contact:index')
    else:
        form = CustomUserCreationForm()
    context = {
        'form': form,
        'form_action': form_action
    }
    return render(
        request,
        'contact/register.html',
        context
    )
    
def login_view(request):
    form_action = reverse('contact:login')
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth.login(request, user)
            messages.success(request, 'Login realizado com sucesso!')
            return redirect('contact:index')
    else:
        form = AuthenticationForm()
    context = {
        'form': form,
        'form_action': form_action
    }
    return render(
        request,
        'contact/login.html',
        context
    )
    
@login_required(login_url='contact:login')
def logout_view(request):
    auth.logout(request)
    return redirect('contact:login')

@login_required(login_url='contact:login')
def user_update(request):
    form_action = reverse('contact:user_update')
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Usuario atualizado com sucesso!')
            return redirect('contact:index')
    else:
        form = UserUpdateForm(instance=request.user)
    context = {
        'form': form,
        'form_action': form_action
    }
    return render(
        request,
        'contact/user_update.html',
        context
    )
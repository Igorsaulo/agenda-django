from django.shortcuts import render, redirect, get_object_or_404
from contact.models import Contact
from contact.forms import ContactForm
from django.urls import reverse
from django.contrib.auth.decorators import login_required

@login_required(login_url='contact:login')
def create(request):
    form_action = reverse('contact:create')
    
    if request.method == 'POST':
        form = ContactForm(request.POST, request.FILES)
        if form.is_valid():
            contact = form.save(commit=False)
            contact.owner = request.user
            contact.save()
            return redirect(f'/contact/{contact.id}/update/')
    else:
        form = ContactForm()
        
    context = {
        'form': form,
        'form_action': form_action
    }
    
    return render(
        request,
        'contact/create.html',
        context
    )

@login_required(login_url='contact:login')
def update(request, contact_id):
    contact = get_object_or_404(Contact, id=contact_id, show=True)
    form = ContactForm(request.POST or None, request.FILES or None, instance=contact)
    if form.is_valid():
        form.save()
        return redirect('contact:index')
    return render(
        request,
        'contact/create.html',
        {'form': form}
    )

@login_required(login_url='contact:login')
def delete(request, contact_id):
    contact = get_object_or_404(Contact, id=contact_id, show=True)
    confirmation = request.POST.get('confirmation', 'no')
    if confirmation == 'yes':
        if contact.picture:
            contact.picture.delete()
        contact.delete()
        return redirect('contact:index')
    
    context = {
        'contact': contact,
        'confirmation': confirmation
    }
    return render(
        request,
        'contact/contact.html',
        context
    )
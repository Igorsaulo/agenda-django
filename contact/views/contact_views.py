from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from contact.models import Contact
from django.core.paginator import Paginator


size = 10

def index(request):
    contacts = Contact.objects.filter(show=True).order_by('-id')
    paginator = Paginator(contacts, size)
    page = request.GET.get('page')
    contacts = paginator.get_page(page)
    
    return render(
        request, 
        'contact/index.html',
        {'contacts': contacts})
    
def contact(request, contact_id):
    single_contact = get_object_or_404(Contact, id=contact_id, show=True)
    
    site_title = f'{single_contact.first_name} {single_contact.last_name} - '

    context = {
        'contact': single_contact,
        'site_title': site_title
    }
    
    return render(
        request,
        'contact/contact.html',
        context
        )
    
def textDivisible(text : str) -> bool:
    return len(text.split(' ')) == 2

def search(request):
    query = request.GET.get('q').strip()
    
    if query == '':
        return redirect('contact:index')
    contacts = Contact.objects.filter(show=True).filter(
        Q(first_name__icontains=query) 
        | Q(last_name__icontains=query)
        | Q(email__icontains=query)
        | Q(phone__icontains=query)
        | (Q(first_name__icontains=query.split(' ')[0]) & Q(last_name__icontains=query.split(' ')[1])) if textDivisible(query) else Q()
            
        
    ).order_by('-id')
    context = {
        'contacts': contacts,
        'site_title': f'Resultados para {query} -'
    }
    
    return render(
        request,
        'contact/index.html',
        context
    )

def split_len(text : str) -> bool:
    return len(text.split(' ')) == 2
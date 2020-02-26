"""
Definition of views.
"""

from datetime import datetime
from django.shortcuts import render, redirect
from django.http import HttpRequest
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from .models import order
from django.contrib.auth import get_user
from .forms import SignUpForm, OrderForm, EstimateForm
from django.contrib import messages
from django.utils.timezone import datetime #important if using timezones
from django.core.mail import EmailMessage
from django.shortcuts import render
from django.conf import settings
from django.core.files.storage import FileSystemStorage
import os

def estimate(request):
    if request.method == 'POST' and request.FILES:
       
        myfile = request.FILES['file']

        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        form = EstimateForm(request.POST)
        if form.is_valid():
            message = 'Hello ' + form.cleaned_data.get('firstName')
            message += '\n\nProblem Statement:\n' + form.cleaned_data.get('description')
            message += '\n\nThank you for submitting an estimate with us, we will reach out to you shortly with a response!'
            
            #message += '\nFile:\n' + myfile
            emailmsg = EmailMessage('Printing Estimate', message, to=[form.cleaned_data.get('email')],bcc=['benvcovey@gmail.com'])
            base_dir = 'C:\\'  
            emailmsg.attach_file(os.path.join(base_dir,uploaded_file_url))
            emailmsg.send()
            messages.info(request, 'Your Estimate has been sent successfully!')
            redirect('app/index.html')
            return render(request, 'app/index.html',
                {
                    'title':'Home Page',
                    'year':datetime.now().year,
                }
            )
        else:
            messages.error(request, 'Please fill out First Name, Email and Description to send for an estimate.')
            return redirect('home')
    else:
         form = EstimateForm(request.POST)
         if form.is_valid():
            message = 'Hello ' + form.cleaned_data.get('firstName')
            message += '\n\nProblem Statement:\n' + form.cleaned_data.get('description')
            message += '\n\nThank you for submitting an estimate with us, we will reach out to you shortly with a response!'
            emailmsg = EmailMessage('Printing Estimate', message, to=[form.cleaned_data.get('email')],bcc=['benvcovey@gmail.com'])
            emailmsg.send()
            messages.info(request, 'Your Estimate has been sent successfully!')
            return redirect('home')
         else:
            messages.error(request, 'Please fill out First Name, Email and Description to send for an estimate.')
            return redirect('home')



def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/index.html',
        {
            'title':'Home Page',
            'year':datetime.now().year,
        }
    )

def contact(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/contact.html',
        {
            'title':'Contact',
            'message':'Your contact page.',
            'year':datetime.now().year,
        }
    )

@login_required(login_url='/login/')
def orders(request):
    username = None
    if request.user.is_authenticated:
        username = request.user.username
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    
    print('User signed in: '+username)
    all_objects = order.objects.filter(ORDER_USER=username).order_by('-ID') #(ORDER_USER=username)
    context= {'orders': all_objects}
    print(context)
    return render(
        request,
        'app/orders.html',
        {
            'title':'Orders',
            'message':'Place/View an order on the website',
            'year':datetime.now().year,
            'orders':all_objects,
        },
        
    )

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('orders')
    else:
        form = SignUpForm()
    return render(request, 'app/signup.html', {'form': form})

def neworder(request):
     username = None
     email = None
     if request.user.is_authenticated:
         username = request.user.username
         email = request.user.email
     #Get Variables
     
     if request.method == 'POST':
        print('New Order inside Post')
        form = OrderForm(request.POST)
        if form.is_valid():
            orderName = form.cleaned_data.get('newOrder')
            if orderName is None:
                orderName = "OrderName"
            orderDescription = form.cleaned_data.get('description')
            if orderDescription is None:
                orderDescription = "None"
            orderLink = form.cleaned_data.get('link')
            if orderLink is None:
                orderLink = "None"
            #form.save()
            newOrder = order()
            newOrder.ORDER_NAME = orderName
            newOrder.DESCRIPTION = orderDescription
            newOrder.LINK = orderLink
            newOrder.ORDER_USER = username
            newOrder.ORDER_DATE = datetime.today()
            newOrder.ORDER_DATE_COMPLETED = 'TBD'
            newOrder.ORDER_DATE_DELIVERED = 'TBD'
            newOrder.COST_CHARGED = 'TBD'
            newOrder.COST_ESTIMATED = 'TBD'
            newOrder.ORDER_STATUS = 'Created'
            newOrder.save()
            messages.info(request, 'Your Order has been sent successfully!')
            #Email out
                #DataFlair
            #EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
            #EMAIL_HOST = 'smtp.gmail.com'
            #EMAIL_USE_TLS = True
            #EMAIL_PORT = 587
            #EMAIL_HOST_USER = 'benvcovey3dprinting@gmail.com'
            #EMAIL_HOST_PASSWORD = 'Ben@1108'
            subject = '3D Printing Order: ' + form.cleaned_data.get('newOrder')
            message = 'Thank you for placing an order! Please reply to this email with ideas you would like to print, files, or links to items you want to come to life!'
            message += '\n\nIf you have any questions or concerns please reach out to me via email or text/call at (902)292-6862'
            message += '\n\nOrder Information Submitted:'
            message += '\nOrder Name: ' + orderName
            message += '\nOrder Description: ' + orderDescription
            message += '\nOrder Link(s): ' + orderLink
            message += '\n\nThank you'
            message += '\nBen Covey'
            print(email)
            emailmsg = EmailMessage(subject, message, to=[email])
            emailmsg.send()

            messages.info(request, 'Automated email has been sent regarding your order!')
            return redirect('orders')
        else:
            messages.info(request, 'Your Order has failed to send, ensure Order Name and Description are filled.')
            return redirect('orders')
   
    
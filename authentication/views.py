from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseBadRequest
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.mail import EmailMessage, send_mail
from foundlost import settings
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth import authenticate, login, logout
from authentication.tokens import generate_token
from service.models import contactenquiry
from django.shortcuts import render, redirect
from django.http import JsonResponse


from django.http import HttpResponse
from service.models import lost_item,found_item

# Create your views here.
def home(request):
    return render(request, "authentication/index.html")

def signup(request):
    if request.method == "POST":
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']
        
        email_domain = email.split('@')[-1]

        # Check if the email domain is "banasthali.in"
        if email_domain != 'banasthali.in':
            messages.error(request, 'Invalid email domain. Only banasthali.in email addresses are allowed.')
            return redirect('home')

        if User.objects.filter(username=username):
            messages.error(request, "Username already exist! Please try some other username.")
            return redirect('home')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email Already Registered!!")
            return redirect('home')
        
        if len(username)>20:
            messages.error(request, "Username must be under 20 charcters!!")
            return redirect('home')
        
        if pass1 != pass2:
            messages.error(request, "Passwords didn't matched!!")
            return redirect('home')
        
        if not username.isalnum():
            messages.error(request, "Username must be Alpha-Numeric!!")
            return redirect('home')
        
        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name = fname
        myuser.last_name = lname
        # myuser.is_active = False
        myuser.is_active = False
        myuser.save()
        messages.success(request, "Your Account has been created succesfully!! Please check your email to confirm your email address in order to activate your account\n.")
        
        # Welcome Email
        subject = "Welcome to lost and found Login!!"
        message = "Hello " + myuser.first_name + "!! \n" + "Welcome to lost and found!! \nThank you for visiting our website\n. We have also sent you a confirmation email, please confirm your email address. \n\nThanking You\n lost and found dept"        
        from_email = settings.EMAIL_HOST_USER
        to_list = [myuser.email]
        send_mail(subject, message, from_email, to_list, fail_silently=True)
        
        # Email Address Confirmation Email
        current_site = get_current_site(request)
        email_subject = "Confirm your Email @ lost and found Login!!"
        message2 = render_to_string('email_confirmation.html',{
            
            'name': myuser.first_name,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(myuser.pk)),
            'token': generate_token.make_token(myuser)
        })
        email = EmailMessage(
        email_subject,
        message2,
        settings.EMAIL_HOST_USER,
        [myuser.email],
        )
        email.fail_silently = True
        email.send()
        
        return redirect('signin')
        
        
    return render(request, "authentication/signup.html")



  # Import HttpResponse for temporary debugging

def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        myuser = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        myuser = None

    if myuser is not None and generate_token.check_token(myuser, token):
        myuser.is_active = True
        myuser.save()
        login(request, myuser)
        messages.success(request, "Your Account has been activated!!")
        return redirect('signin')
    else:
        print("Activation Failed: uid={}, token={}".format(uidb64, token))  # Debugging statement
        return render(request, 'activation_failed.html')


def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        pass1 = request.POST['pass1']
        
        user = authenticate(username=username, password=pass1)
        
        if user is not None:
            login(request, user)
            fname = user.first_name
            # messages.success(request, "Logged In Sucessfully!!")
            return render(request, "authentication/l.html", {"fname": fname})
        else:
            messages.error(request, "Bad Credentials!!")
            return redirect('home')
    
    return render(request, "authentication/signin.html")


def save_lost_item(request):
    if request.method == 'POST':
        try:
            # Extract form data from the request
            category = request.POST.get('item-category')
            date = request.POST.get('date')
            location = request.POST.get('location')
            size = request.POST.get('size')
            specific_mark = request.POST.get('specificMark')
            shape = request.POST.get('shape')
            color = request.POST.get('color')
            brand = request.POST.get('brand')
            material = request.POST.get('material')
            image = request.FILES.get('image') 
            # Create a new LostItem instance
            new_lost_item = lost_item.objects.create(
                item_category=category,
                date=date,
                location=location,
                size=size,
                specific_mark=specific_mark,
                shape=shape,
                color=color,
                brand=brand,
                material=material,
                image=image
            )
            # No need to call lost_item.save() as it's already saved by create()

            return render(request, 'authentication/response.html')
        except Exception as e:
            # Handle any exceptions and render an error page
            return render(request, 'error.html', {'error_message': str(e)})
    else:
        # Handle invalid request method
        return render(request, 'error.html', {'error_message': 'Invalid request method'})
def save_found_item(request):
    if request.method == 'POST':
        try:
            # Extract form data from the request
            category = request.POST.get('item-category')
            date = request.POST.get('date')
            location = request.POST.get('location')
            size = request.POST.get('size')
            specific_mark = request.POST.get('specificMark')
            shape = request.POST.get('shape')
            color = request.POST.get('color')
            brand = request.POST.get('brand')
            material = request.POST.get('material')
            
            # Create a new LostItem instance
            new_found_item = found_item.objects.create(
                item_category=category,
                date=date,
                location=location,
                size=size,
                specific_mark=specific_mark,
                shape=shape,
                color=color,
                brand=brand,
                material=material
            )
            # No need to call lost_item.save() as it's already saved by create()

            return JsonResponse({'success': True})  # Return success response
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)
    else:
        # Handle invalid request method
        return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=405)
def savefound(request):
    return render(request,"index.html")
def saveenqury(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        en=contactenquiry(name=name,email=email,message=message)
        en.save()
        subject = 'Contact Form Submission'
        message = f'Name: {name}\nEmail: {email}\nMessage: {message}'
        sender_email = settings.EMAIL_HOST_USER
        recipient_list = [settings.CONTACT_EMAIL]  # Add your email address here
        send_mail(subject, message, sender_email, recipient_list)
    return render(request,"thank_you.html")

def response(request):
    return render(request, 'response.html')
def thank_you(request):
    return render(request, 'thank_you.html')
def phone_page(request):
    # Your view logic here
    return render(request, 'thank_you.html')
def contact_page(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        # Send email
        subject = 'Contact Form Submission'
        message = f'Name: {name}\nEmail: {email}\nMessage: {message}'
        sender_email = settings.EMAIL_HOST_USER
        recipient_list = [settings.CONTACT_EMAIL]  # Add your email address here
        send_mail(subject, message, sender_email, recipient_list)
        return render(request, 'thank_you.html')

    return render(request, 'contact.html')
def l(request):
    return render(request, 'l.html')
def about(request):
    return render(request, 'about.html')
def lost(request):
    return render(request, 'authentication/lost.html')
def found(request):
    return render(request, 'authentication/found.html')
def signout(request):
    logout(request)
    messages.success(request, "Logged Out Successfully!!")
    return redirect('home')

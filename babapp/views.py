from django.shortcuts import render,redirect
from babapp.models import register as re
from django.contrib.auth.hashers import check_password ,make_password
from babapp.forms import regform,forgotform,passform
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import PasswordResetView
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.core.mail import send_mail,EmailMultiAlternatives
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags




# Create your views here.
def index(request):
    return render(request,'index.html')
def login(request):
    return render(request,'login.html')

def register(request):
    if request.method=='POST':
        fm=regform(request.POST)
        if fm.is_valid():
            password=fm.cleaned_data['password']
            hashed_password=make_password(password)
            new_user=fm.save(commit=False)
            new_user.password=hashed_password
            new_user.save()
            return redirect('login')
    else:
        fm = regform()
      
    return render(request,'register.html',{'register': fm})
def verify(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        try:
            user1 = re.objects.get(Email=email)
        except re.DoesNotExist:
            # User with the given email does not exist
            return render(request, 'login.html', {'error': 'Invalid email or password'})
        except Exception as e:
        #     # Handle unexpected exceptions, e.g., database connection issues
            print(e)
            return render(request, 'login.html', {'error': 'An unexpected error occurred'})

        # Verify the password
        if check_password(password, user1.password):
            # Password is correct, proceed with login
            # Set session or user authentication here
            # Redirect to a success page or home page
            return redirect('home')  # Replace 'home' with your actual URL name for the home page
        else:
            # Password is incorrect
            return render(request, 'login.html', {'error': 'Invalid email or password'})
    else:
        # Render the login form
        return render(request, 'login.html')
def home(request):
    return render(request,'home.html')
def forgot(request):
    if request.method == 'POST':
        form = forgotform(request.POST)
        if form.is_valid():
            email = form.cleaned_data['Email']
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                return render(request, 'forgot.html', {'error': 'Invalid email address'})
            
            # Generate and send password reset email
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)
            current_site = get_current_site(request)
            protocol = 'http' if not request.is_secure() else 'https'
            reset_url = f"{protocol}://{current_site.domain}{reverse('password_reset_confirm', kwargs={'uidb64': uid, 'token': token})}"
            mail_subject = 'Reset your password'
            context = {
                'reset_url': reset_url
            }
            html_message = render_to_string('password.html', context)
            text_message = strip_tags(html_message)
            email = EmailMultiAlternatives(
                subject=mail_subject,
                body=text_message,
                from_email=settings.EMAIL_HOST_USER,
                to=[user.email],
            )
            email.attach_alternative(html_message, "text/html")  # Attach HTML content
            email.send()
            
            return render(request,'password_reset_email.html',{'sent':'email sent'})
            
            
    else:
        form = forgotform()
    return render(request, 'forgot.html', {'form': form})
def password(request):
    return render(request,'password.html')
def password_reset_email(request):
    return render(request,'password_reset_email.html')



    
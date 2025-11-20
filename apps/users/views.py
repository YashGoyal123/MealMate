"""
Views for email verification and user management
"""
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model, logout, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.views.decorators.http import require_http_methods
from allauth.account.forms import SignupForm
from .models import EmailVerificationOTP
from .forms import ProfileUpdateForm

User = get_user_model()


@require_http_methods(["GET", "POST"])
def send_verification_otp(request):
    """Send OTP to user's email"""
    if request.method == 'POST':
        email = request.POST.get('email')
        
        # Check if user exists
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.error(request, 'No account found with this email.')
            return render(request, 'users/send_otp.html')
        
        # Create OTP
        otp_obj = EmailVerificationOTP.objects.create(
            user=user,
            email=email
        )
        
        # Send email
        try:
            subject = 'MealMate - Email Verification OTP'
            message = f'''
Hello {user.username},

Your OTP for email verification is: {otp_obj.otp}

This OTP will expire in 10 minutes.

If you didn't request this, please ignore this email.

Best regards,
MealMate Team
            '''
            
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [email],
                fail_silently=False,
            )
            
            messages.success(request, f'OTP has been sent to {email}')
            return redirect('users:verify_otp', otp_id=otp_obj.id)
        
        except Exception as e:
            messages.error(request, f'Failed to send OTP: {str(e)}')
            otp_obj.delete()
            return render(request, 'users/send_otp.html')
    
    return render(request, 'users/send_otp.html')


@require_http_methods(["GET", "POST"])
def verify_otp(request, otp_id):
    """Verify OTP entered by user"""
    try:
        otp_obj = EmailVerificationOTP.objects.get(id=otp_id, is_verified=False)
    except EmailVerificationOTP.DoesNotExist:
        messages.error(request, 'Invalid or expired OTP request.')
        return redirect('users:send_otp')
    
    if request.method == 'POST':
        otp_input = request.POST.get('otp', '').strip()
        
        success, message = otp_obj.verify(otp_input)
        
        if success:
            # Mark user's email as verified
            user = otp_obj.user
            if hasattr(user, 'email_verified'):
                user.email_verified = True
                user.save()
            
            messages.success(request, message)
            return redirect('account_login')
        else:
            messages.error(request, message)
    
    context = {
        'otp_obj': otp_obj,
        'email': otp_obj.email,
    }
    return render(request, 'users/verify_otp.html', context)


@require_http_methods(["POST"])
def resend_otp(request, otp_id):
    """Resend OTP to user's email"""
    try:
        old_otp = EmailVerificationOTP.objects.get(id=otp_id)
    except EmailVerificationOTP.DoesNotExist:
        messages.error(request, 'Invalid OTP request.')
        return redirect('users:send_otp')
    
    # Create new OTP
    new_otp = EmailVerificationOTP.objects.create(
        user=old_otp.user,
        email=old_otp.email
    )
    
    # Send email
    try:
        subject = 'MealMate - Email Verification OTP (Resent)'
        message = f'''
Hello {new_otp.user.username},

Your new OTP for email verification is: {new_otp.otp}

This OTP will expire in 10 minutes.

If you didn't request this, please ignore this email.

Best regards,
MealMate Team
        '''
        
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [new_otp.email],
            fail_silently=False,
        )
        
        messages.success(request, f'New OTP has been sent to {new_otp.email}')
        return redirect('users:verify_otp', otp_id=new_otp.id)
    
    except Exception as e:
        messages.error(request, f'Failed to send OTP: {str(e)}')
        new_otp.delete()
        return redirect('users:verify_otp', otp_id=otp_id)


@login_required
@require_http_methods(["POST"])
def delete_account(request):
    """Delete user account permanently"""
    user = request.user
    username = user.username
    
    try:
        # Logout first
        logout(request)
        
        # Delete the user (this will cascade delete all related data)
        user.delete()
        
        messages.success(
            request, 
            f'Account "{username}" has been permanently deleted. We\'re sorry to see you go!'
        )
    except Exception as e:
        messages.error(request, f'Failed to delete account: {str(e)}')
        return redirect('home')
    
    return redirect('home')


@require_http_methods(["GET", "POST"])
def custom_signup(request):
    """Custom signup that requires OTP verification before account creation"""
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        
        # Basic validation
        if not all([username, email, password1, password2]):
            messages.error(request, 'All fields are required.')
            return render(request, 'account/signup.html')
        
        if password1 != password2:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'account/signup.html')
        
        if len(password1) < 8:
            messages.error(request, 'Password must be at least 8 characters long.')
            return render(request, 'account/signup.html')
        
        # Check if username already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
            return render(request, 'account/signup.html')
        
        # Check if email already exists
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered.')
            return render(request, 'account/signup.html')
        
        # Store signup data in session
        request.session['pending_signup'] = {
            'username': username,
            'email': email,
            'password': password1,
        }
        
        # Create OTP for verification (without creating user yet)
        otp_obj = EmailVerificationOTP.objects.create(
            user=None,  # No user yet
            email=email
        )
        
        # Send OTP email
        try:
            subject = 'MealMate - Verify Your Email to Complete Signup'
            message = f'''
Hello {username},

Welcome to MealMate! 

To complete your account creation, please verify your email address using the OTP below:

Your OTP: {otp_obj.otp}

This OTP will expire in 10 minutes.

If you didn't sign up for MealMate, please ignore this email.

Best regards,
MealMate Team
            '''
            
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [email],
                fail_silently=False,
            )
            
            messages.success(request, f'Verification OTP has been sent to {email}. Please check your email.')
            
            return redirect('users:verify_signup_otp', otp_id=otp_obj.id)
        
        except Exception as e:
            messages.error(request, f'Failed to send OTP: {str(e)}')
            otp_obj.delete()
            return render(request, 'account/signup.html')
    
    return render(request, 'account/signup.html')


@require_http_methods(["GET", "POST"])
def verify_signup_otp(request, otp_id):
    """Verify OTP and create user account"""
    # Get pending signup data from session
    pending_signup = request.session.get('pending_signup')
    if not pending_signup:
        messages.error(request, 'Signup session expired. Please sign up again.')
        return redirect('account_signup')
    
    try:
        otp_obj = EmailVerificationOTP.objects.get(id=otp_id, is_verified=False)
    except EmailVerificationOTP.DoesNotExist:
        messages.error(request, 'Invalid or expired OTP request.')
        return redirect('account_signup')
    
    # Verify email matches
    if otp_obj.email != pending_signup['email']:
        messages.error(request, 'Email mismatch. Please sign up again.')
        return redirect('account_signup')
    
    if request.method == 'POST':
        otp_input = request.POST.get('otp', '').strip()
        
        success, message = otp_obj.verify(otp_input)
        
        if success:
            # Create the user account now
            try:
                user = User.objects.create_user(
                    username=pending_signup['username'],
                    email=pending_signup['email'],
                    password=pending_signup['password']
                )
                user.email_verified = True
                user.save()
                
                # Link OTP to user
                otp_obj.user = user
                otp_obj.save()
                
                # Clear session data
                del request.session['pending_signup']
                
                # Log the user in
                login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                
                messages.success(request, f'Welcome {user.username}! Your account has been created successfully.')
                return redirect('home')
            
            except Exception as e:
                messages.error(request, f'Failed to create account: {str(e)}')
                return render(request, 'users/verify_signup_otp.html', {
                    'otp_obj': otp_obj,
                    'email': otp_obj.email,
                })
        else:
            messages.error(request, message)
    
    context = {
        'otp_obj': otp_obj,
        'email': otp_obj.email,
        'username': pending_signup['username'],
    }
    return render(request, 'users/verify_signup_otp.html', context)


@require_http_methods(["POST"])
def resend_signup_otp(request, otp_id):
    """Resend OTP during signup"""
    pending_signup = request.session.get('pending_signup')
    if not pending_signup:
        messages.error(request, 'Signup session expired. Please sign up again.')
        return redirect('account_signup')
    
    try:
        old_otp = EmailVerificationOTP.objects.get(id=otp_id)
    except EmailVerificationOTP.DoesNotExist:
        messages.error(request, 'Invalid OTP request.')
        return redirect('account_signup')
    
    # Create new OTP
    new_otp = EmailVerificationOTP.objects.create(
        user=None,
        email=old_otp.email
    )
    
    # Send email
    try:
        subject = 'MealMate - Verify Your Email (OTP Resent)'
        message = f'''
Hello {pending_signup['username']},

Your new OTP for email verification is: {new_otp.otp}

This OTP will expire in 10 minutes.

If you didn't request this, please ignore this email.

Best regards,
MealMate Team
        '''
        
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [new_otp.email],
            fail_silently=False,
        )
        
        messages.success(request, f'New OTP has been sent to {new_otp.email}')
        return redirect('users:verify_signup_otp', otp_id=new_otp.id)
    
    except Exception as e:
        messages.error(request, f'Failed to send OTP: {str(e)}')
        new_otp.delete()
        return redirect('users:verify_signup_otp', otp_id=otp_id)


@login_required
def profile_update(request):
    """View for updating user profile"""
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('users:profile_update')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ProfileUpdateForm(instance=request.user)
    
    context = {
        'form': form,
        'user': request.user,
    }
    return render(request, 'users/profile_update.html', context)

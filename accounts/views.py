from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import Profile
from django.core.mail import send_mail
from .models import EmailOTP
import random
import os
from django.conf import settings

EMAIL_ENABLED = os.getenv("EMAIL_ENABLED") == "True"

def signup(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect('signup')

        # if User.objects.filter(email=email).exists():
        #     messages.error(request, "Email already registered.")
        #     return redirect('signup')

        otp = str(random.randint(100000, 999999))

        EmailOTP.objects.update_or_create(
            email=email,
            defaults={'otp': otp}
        )

        subject = "Your Waste2Wealth OTP Verification Code"
        message = f"""
Hello {username},

Your OTP for Waste2Wealth signup is: {otp}

This OTP is valid for 10 minutes.
If you did not request this, please ignore this email.

Regards,
Waste2Wealth Team
"""

        if EMAIL_ENABLED:
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [email],
                fail_silently=False,
            )
        else:
            print("OTP for", email, "is:", otp)

        request.session['signup_username'] = username
        request.session['signup_email'] = email
        request.session['signup_password'] = password

        return redirect('verify_otp')

    return render(request, "accounts/signup.html")


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid credentials')
            return redirect('login')

    return render(request, 'accounts/login.html')


def logout_view(request):
    logout(request)
    return redirect('home')

def verify_otp(request):
    if request.method == "POST":
        entered_otp = request.POST.get("otp")

        username = request.session.get('signup_username')
        email = request.session.get('signup_email')
        password = request.session.get('signup_password')

        try:
            record = EmailOTP.objects.get(email=email)

            if record.is_expired():
                messages.error(request, "OTP expired. Please sign up again.")
                return redirect('signup')

            if record.otp == entered_otp:
                User.objects.create_user(
                    username=username,
                    email=email,
                    password=password
                )

                # Cleanup
                record.delete()
                request.session.flush()

                messages.success(request, "Account created successfully!")
                return redirect('login')

            else:
                messages.error(request, "Invalid OTP")

        except EmailOTP.DoesNotExist:
            messages.error(request, "OTP not found")

    return render(request, "accounts/verify_otp.html")

from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from .models import species,services,Schedule,Diagnosis,CustomUser
from decimal import Decimal
import json
from django.core.paginator import Paginator
from datetime import datetime, timedelta
from django.http import JsonResponse
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from django.conf import settings
from django.http import HttpResponse
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from smtplib import SMTPException

from django.urls import reverse

from django.contrib.auth import get_user_model,logout,login,authenticate #Use for User Authentication
from django.contrib.auth.decorators import login_required #to prevent bypassing
from django.contrib.auth.hashers import make_password,check_password #hashed password


User = get_user_model()
    


def generate_reset_token(email):
    try:
        user = CustomUser.objects.get(email=email)
        uid = urlsafe_base64_encode(force_bytes(user.pk))  
        token = default_token_generator.make_token(user)  
        return uid, token
    except CustomUser.DoesNotExist:
        return None, None

def logout_view(request):
    logout(request)  # Clear the session and logout the user
    return redirect('index')  

#LOGIN

def index(request):
    if request.method == 'POST':
        email = request.POST.get('email').strip()
        password = request.POST.get('password')

        # Check if email and password are provided
        if not email or not password:
            messages.error(request, 'Both email and password are required.')
            return render(request, 'login.html')

        # Check if the email is 'admin@gmail.com' and password is 'admin'
        if email == 'admin@gmail.com' and password == 'admin':
            request.session['fname'] = 'Admin'
            request.session['email'] = email
            request.session['is_admin'] = True
            return redirect('admin')  # Redirect to admin's homepage URL

        # Check if the email is 'vet@gmail.com' and password is 'vet'
        if email == 'vet@gmail.com' and password == 'vet':
            request.session['fname'] = 'Vet'
            request.session['email'] = email
            request.session['is_vet'] = True
            return redirect('vet')  # Redirect to vet's homepage URL

        # Authenticate the user for other email/password combinations
        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)
            request.session['email'] = user.email
            return redirect('owner')  # Redirect to owner's homepage URL
        else:
            # Check if email or password is incorrect (combine the error message)
            messages.error(request, 'Invalid email or password.')

            return render(request, 'login.html')

    return render(request, 'login.html')

   

@login_required(login_url='index')  
def owner(request):
    # Fetch pending appointments for the logged-in user
    pending_appointments = Schedule.objects.filter(
        account=request.user,
        status='Pending'
    )
    
    # Fetch the first name of the logged-in user (CustomUser model)
    fname = request.user.fname
    
    # Set session flag for showing greeting message (only once per session)
    if not request.session.get('greeting_shown', False):
        request.session['greeting_shown'] = True
        show_greeting = True
    else:
        show_greeting = False
    
    return render(request, 'homepage.html', {
        'pending_appointments': pending_appointments,
        'fname': fname,
        'show_greeting': show_greeting,  # Add the flag to context
    })





@login_required(login_url='index')  # Redirect to the login page if not logged in
def profile(request):
    if 'email' in request.session:
        email = request.session['email']

        # Check if the email is admin or a normal user
        if email == 'admin@gmail.com':
            context = {
                'first_name': '',
                'last_name': '',
                'email': '',    
                'phone_number': '',
            }
            return render(request, "profile.html", context)

        try:
            # Fetch user details based on the session's email
            account = CustomUser.objects.get(email=email)

            if request.method == 'POST':
                # Collect data from the form, excluding password and confirm_password
                new_fname = request.POST.get('fname')
                new_lname = request.POST.get('lname')
                new_email = request.POST.get('email')
                new_number = request.POST.get('phone')

                # Update the database if changes are detected
                if (account.fname != new_fname or account.lname != new_lname or
                        account.email != new_email or
                        account.number != new_number):
                    account.fname = new_fname
                    account.lname = new_lname
                    account.email = new_email
                    account.number = new_number
                    account.save()

                    return redirect('owner')  # Redirect to 'owner' after successful profile update

                messages.info(request, 'No changes were made.')
                return redirect('profile')

            context = {
                'first_name': account.fname,
                'last_name': account.lname,
                'email': account.email,
                'phone_number': account.number,
            }
            return render(request, "profile.html", context)

        except CustomUser.DoesNotExist:
            messages.error(request, 'Account not found. Please log in again.')
            return redirect('index')
    else:
        messages.error(request, 'You need to log in first.')
        return redirect('index')

    


def registration(request):
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')
        first_name = request.POST.get('fname', '')
        last_name = request.POST.get('lname', '')
        number = request.POST.get('phone', '')
        confirm_password = request.POST.get('confirm_password', '')

        if password != confirm_password:
            return render(request, 'reg.html', {'error': 'Passwords do not match'})

        if CustomUser.objects.filter(email=email).exists():
            return render(request, 'reg.html', {'error': 'Email is already used'})

        # Create the new account using CustomUserManager
        new_account = CustomUser.objects.create_user(
            email=email,
            password=password,  # Password will be hashed automatically
            fname=first_name,
            lname=last_name,
            number=number
        )
        new_account.save()

        # Redirect to index page after successful registration
        return redirect('index') 

    return render(request, 'reg.html')




def forgot(request):
    if request.method == 'GET' and 'email' in request.GET:
        email = request.GET.get('email')

        # Check if the email exists in the Accounts model
        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            # If the email does not exist, show a notification
            return render(request, 'forgotPass.html', {'error': 'Email not found.'})

        if user:
            token = default_token_generator.make_token(user)
            current_site = get_current_site(request).domain
            encoded_email = urlsafe_base64_encode(force_bytes(user.email))
            reset_link = f"http://{current_site}/reset-password/{encoded_email}/{token}"

            subject = "Password Reset Request"
            body = f"""
            <html>
                <body style="font-family: Arial, sans-serif; background-color: #1A1A1A; color: white; text-align: center; padding: 0;">
                    <div style="max-width: 600px; margin: auto; background-color: #1A1A1A; padding: 30px; border-radius: 8px;">
                        <!-- Header Text -->
                        <h2 style="font-size: 28px; font-weight: bold; color: #FF7866; margin-bottom: 20px;">
                            PET CARE VETERINARY CLINIC SYSTEM
                        </h2>

                        <!-- Title -->
                        <h1 style="font-size: 24px; font-weight: bold; color: white; margin-bottom: 20px;">
                            CHANGE YOUR PASSWORD
                        </h1>

                        <!-- Instruction -->
                        <p style="font-size: 16px; color: #CCCCCC; margin-bottom: 30px;">
                            Hello {user.fname},<br>
                            We received a request to reset your password. Click the button below to reset your password.<br><br>
                            If you did not request this, please ignore this email.
                        </p>

                        <!-- Button -->
                        <a href="{reset_link}" style="
                            display: inline-block;
                            text-decoration: none;
                            background-color: #FF7866;
                            color: white;
                            padding: 14px 24px;
                            font-size: 16px;
                            font-weight: bold;
                            border-radius: 5px;
                            box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.2);
                            transition: transform 0.3s ease, box-shadow 0.3s ease;">
                            RESET MY PASSWORD
                        </a>

                        <!-- Footer -->
                        <p style="margin-top: 30px; font-size: 12px; color: #666666;">
                            Â© 2024 PET CARE Veterinary Clinic System
                        </p>
                    </div>
                </body>
            </html>
            """


            # Gmail SMTP setup
            sender_email = settings.EMAIL_HOST_USER
            sender_password = settings.EMAIL_HOST_PASSWORD
            smtp_server = "smtp.gmail.com"
            smtp_port = 587

            try:
                # Setting up the MIME message
                msg = MIMEMultipart()
                msg["From"] = sender_email
                msg["To"] = email
                msg["Subject"] = subject

                # Attach the email body
                msg.attach(MIMEText(body, "html"))

                # Sending email via SMTP
                with smtplib.SMTP(smtp_server, smtp_port) as server:
                    server.starttls()
                    server.login(sender_email, sender_password)  # Login to Gmail
                    server.sendmail(sender_email, email, msg.as_string())  # Send the email

                # Redirect to email confirmation page
                return redirect('email_sent')  # Redirects to the email.html view

            except SMTPException as e:
                return HttpResponse(f"Failed to send email. Error: {str(e)}", status=500)

    return render(request, 'forgotPass.html')


def email_sent(request):
    return render(request, 'email.html')


def reset_password(request, encoded_email, token):
    try:
        # Decode the email from base64
        email = urlsafe_base64_decode(encoded_email).decode('utf-8')

        # Fetch the user based on the email
        user = CustomUser.objects.get(email=email)

        if default_token_generator.check_token(user, token):
            if request.method == 'POST':
                # Get the new password and confirm password
                password = request.POST.get('password')
                confirm_password = request.POST.get('confirm_password')

                # Check if passwords match
                if password == confirm_password:
                    # Hash the password before saving
                    user.password = make_password(password)
                    user.save()

                    return redirect(reverse('index'))
                else:
                    return render(request, 'resetpassword.html', {
                        'error': 'Passwords do not match.',
                        'token': token,
                        'email': encoded_email
                    })
            return render(request, 'resetpassword.html', {'token': token, 'email': encoded_email})
        else:
            return render(request, 'resetpassword.html', {'error': 'Invalid token or email.'})
    except CustomUser.DoesNotExist:
        return render(request, 'resetpassword.html', {'error': 'Invalid email.'})



@login_required(login_url='index')
def adhistory(request):
    return render(request, 'AccountHistory.html')

   
@login_required(login_url='index')
def adaccount(request):
    
    # Fetch all account records with the specific fields
    accounts = CustomUser.objects.all().values('fname', 'lname', 'email', 'password', 'number')

    context = {
        'accounts': accounts  
    }
    
    return render(request, "AccountHistory.html", context)






@login_required(login_url='index')
def diagnosis(request):
    return render(request, "DiagnosisForm.html")

#PENDING APPOINTMENTS
@login_required(login_url='index')
def PendingAppointment(request):
 
    if 'email' not in request.session:
        return redirect('index')  

    # Get the logged-in user's email from the session
    user_email = request.session['email']

    # Find the logged-in user account
    try:
        user_account = CustomUser.objects.get(email=user_email)
    except CustomUser.DoesNotExist:
        return redirect('index') 

    
    appointments = Schedule.objects.filter(account=user_account).exclude(status='Completed')

    if request.method == 'POST':
        
        appointment_id = request.POST.get('cancel_appointment')
        if appointment_id:
            try:
                appointment = Schedule.objects.get(id=appointment_id, account=user_account)
                if appointment.status != 'Completed' and appointment.payment_status != 'Paid':
                    
                    appointment.delete()
                    return redirect('pAppointment')  
            except Schedule.DoesNotExist:
                pass  

 
    return render(request, "pendingAppointment.html", {'appointments': appointments})


from django.http import HttpResponseRedirect
from urllib.parse import urlencode

@login_required(login_url='index')  # Redirect to login if not logged in
def change(request):
    if 'email' not in request.session:
        return redirect('index')

    user_email = request.session['email']
    
    try:
        user_account = CustomUser.objects.get(email=user_email)
    except CustomUser.DoesNotExist:
        return redirect('index')

    if request.method == 'POST':
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        # Validate current password
        if not check_password(current_password, user_account.password):
            return HttpResponseRedirect(f"{reverse('change')}?{urlencode({'status': 'incorrect_current_password'})}")

        # Validate new password and confirm password
        if new_password != confirm_password:
            return HttpResponseRedirect(f"{reverse('change')}?{urlencode({'status': 'password_mismatch'})}")

        # Update the password if everything is correct
        user_account.password = make_password(new_password)
        user_account.save()

        return HttpResponseRedirect(f"{reverse('change')}?{urlencode({'status': 'success'})}")

    return render(request, 'changepass.html')












    
#PETOWNER HISTORY
@login_required(login_url='index')
def ownhistory(request):
    # Ensure the user is logged in by checking the session
    if 'email' not in request.session:
        return redirect('index')  
    
    user_email = request.session['email']
 
    try:
        user_account = CustomUser.objects.get(email=user_email)
    except CustomUser.DoesNotExist:
        return redirect('index')  

    schedules = Schedule.objects.filter(account=user_account).exclude(status='Pending').values(
        'Name', 'date', 'time', 'amount', 'services', 'species', 'status'
    )
    context = {
        'schedules': schedules
    }
    
    return render(request, "PetOwnerHistory.html", context)



#APPOINTMENT WINDOW
@login_required(login_url='index')
def appwindow(request):
    # Fetch pet species and services with their amounts
    pet_species = species.objects.values('animal')
    available_services = services.objects.values('services', 'amount')  

    if request.method == 'POST':
        # Ensure the user is logged in
        if 'email' not in request.session:
            messages.error(request, "You must be logged in to book an appointment.")
            return redirect('index')  

        # Fetch the logged-in user's account
        try:
            user_email = request.session['email']
            user_account = CustomUser.objects.get(email=user_email)
        except CustomUser.DoesNotExist:
            messages.error(request, "User account not found. Please log in again.")
            return redirect('index')
        
        # Check if the user has a pending appointment
        existing_appointment = Schedule.objects.filter(account=user_account, status='Pending').first()
        if existing_appointment:
            # User has an existing pending appointment, prevent further appointment creation
            messages.error(request, "You already have a pending appointment. Please complete it before making a new one.")
            return redirect('appwindow')

        name = request.POST.get('Name')
        date = request.POST.get('date')
        time = request.POST.get('time')
        species_selected = request.POST.get('species')
        service_selected = request.POST.get('services')
        amount_input = request.POST.get('amount')
       
        # Convert amount_input to Decimal
        try:
            amount_input = Decimal(amount_input)
        except (ValueError, TypeError):
            messages.error(request, "Invalid amount format.")
            return redirect('appwindow') 

        # Save the appointment, linking it to the logged-in user's account
        appointment = Schedule(
            account=user_account,
            Name=name,
            date=date,
            time=time,
            species=species_selected,
            services=service_selected,
            amount=amount_input,
            status='Pending',
            payment_status='Unpaid'
        )
        appointment.save()

        # Display a success message for appointment submission
        messages.success(request, "Your appointment has been successfully submitted!")




    # Prepare booked slots for the selected date
    booked_slots = {}
    all_appointments = Schedule.objects.all()
    for appointment in all_appointments:
        date = appointment.date.strftime('%Y-%m-%d')
        if date not in booked_slots:
            booked_slots[date] = []
        booked_slots[date].append(appointment.time)

    context = {
        'pet_species': pet_species,
        'available_services': available_services, 
        'booked_slots': json.dumps(booked_slots),
    }

    return render(request, 'appointmentWindow.html', context)



#DASHBOARD SCHEDULE

from datetime import datetime, timedelta
@login_required(login_url='index')
def dashboard(request):
    # Fetch the week offset from the query parameters
    week_offset = int(request.GET.get('week_offset', 0))

    # Determine the start of the week (Monday)
    today = datetime.today()
    today_date = today.strftime('%Y-%m-%d')  # Format today's date to pass to the template

    start_of_week = today + timedelta(days=week_offset * 7 - today.weekday())

    # Generate the dates for the current week (Monday to Sunday)
    week_days = []
    for i in range(7):
        day_date = start_of_week + timedelta(days=i)
        week_days.append({
            'name': day_date.strftime('%A'),  
            'date': day_date.strftime('%Y-%m-%d'),  
            'is_past': day_date < today,  
            'times': []  
        })

    # Fetch all appointments from the database
    appointments = Schedule.objects.all()

    # Prepare the data for occupied slots
    occupied_slots = {}
    for appointment in appointments:
        date = appointment.date.strftime('%Y-%m-%d')
        time = appointment.time
        if date not in occupied_slots:
            occupied_slots[date] = []
        occupied_slots[date].append(time)

    # Populate the occupied times for each day in the week
    for day in week_days:
        if day['date'] == today.strftime('%Y-%m-%d'):
            # Clear the times for today
            day['times'] = []
        elif not day['is_past']:  # Only populate future days
            day['times'] = occupied_slots.get(day['date'], [])

    return render(request, 'Dashboard.html', {
        'week_days': week_days,  
        'week_offset': week_offset,  
        'today_date': today_date,  # Pass today's date to the template
    })








# Custom decorator for admin users
def admin_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if request.session.get('is_admin', False):
            return view_func(request, *args, **kwargs)
        else:
            return redirect('index')  # Redirect to login page if not admin
    return _wrapped_view




from django.http import JsonResponse




@admin_required
@csrf_exempt
def admin(request):
    species_notification = None
    services_notification = None

    if request.method == "POST":
        # Add New Species
        if "edit-species" in request.POST:
            new_species_name = request.POST.get("new-species").strip()
            if new_species_name:
                # Check if species already exists
                if not species.objects.filter(animal=new_species_name).exists():
                    new_species = species(animal=new_species_name)
                    new_species.save()
                    species_notification = "Species added successfully."
                else:
                    species_notification = "Species already exists."

        # Delete Species
        if "delete-species" in request.POST:
            species_name = request.POST.get("current-species")
            if species_name:
                deleted_count, _ = species.objects.filter(animal=species_name).delete()
                if deleted_count > 0:
                    species_notification = f"Species '{species_name}' deleted successfully."
                else:
                    species_notification = "Species not found."

        # Add New Services
        if "edit-services" in request.POST:
            new_service_name = request.POST.get("new-services").strip()
            new_service_amount = request.POST.get("service-amount", "0").strip()

            if new_service_name:
                try:
                    new_service_amount = float(new_service_amount) if new_service_amount else 0.0
                    # Check if service already exists
                    if not services.objects.filter(services=new_service_name).exists():
                        new_service = services(services=new_service_name, amount=new_service_amount)
                        new_service.save()
                        services_notification = "Service added successfully."
                    else:
                        services_notification = "Service already exists."
                except ValueError:
                    services_notification = "Invalid amount value provided."

        # Delete Services
        if "delete-services" in request.POST:
            service_name = request.POST.get("current-services")
            if service_name:
                deleted_count, _ = services.objects.filter(services=service_name).delete()
                if deleted_count > 0:
                    services_notification = f"Service '{service_name}' deleted successfully."
                else:
                    services_notification = "Service not found."

        # Mark payment status as paid
        if "mark-paid" in request.POST:
            schedule_id = request.POST.get("schedule_id")
            try:
                schedule = Schedule.objects.get(id=schedule_id)
                schedule.payment_status = "Paid"
                schedule.status = "Completed"
                schedule.save()
                
            except Schedule.DoesNotExist:
                services_notification = "Schedule not found."

    # Pagination for schedules
    all_schedules = Schedule.objects.all()
    paginator = Paginator(all_schedules, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Fetch all species and services to display
    all_species = species.objects.all()
    all_services = services.objects.all()

    return render(request, 'AppointSched.html', {
        'species': all_species,
        'services': all_services,
        'page_obj': page_obj,
        'species_notification': species_notification,  # Pass species notification
        'services_notification': services_notification  # Pass services notification
    })



@admin_required
def adaccount(request):
    
    # Fetch all account records with the specific fields
    accounts = CustomUser.objects.all().values('fname', 'lname', 'email', 'number')

    context = {
        'accounts': accounts  
    }
    
    return render(request, "AccountHistory.html", context)



@admin_required
def trans(request):
    # Fetch only the required fields
    schedules = Schedule.objects.values('date', 'amount', 'services', 'species', 'Name')

    context = {
        'schedules': schedules
    }
    
    return render(request, "Transaction_history.html", context)



# Custom decorator for vet users
def vet_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if request.session.get('is_vet', False):
            return view_func(request, *args, **kwargs)
        else:
            return redirect('index') 
    return _wrapped_view

from django.shortcuts import render, get_object_or_404

@vet_required
def vetHistory(request):
    # Fetch all diagnoses from the database
    diagnoses = Diagnosis.objects.all()

    # Pass the diagnoses data to the template
    context = {
        'diagnoses': diagnoses
    }

    return render(request, "vet_history.html", context)

def diagnosis_detail(request, diagnosis_id):
    # Get the specific diagnosis based on the ID
    diagnosis = get_object_or_404(Diagnosis, pk=diagnosis_id)

    # Pass the diagnosis data to the history template
    return render(request, "history.html", {'diagnosis': diagnosis})


@vet_required
def vet(request):
    """
    View to handle vet window operations, including fetching schedules and saving diagnoses.
    """
    # Fetch all schedules from the Schedule model
    all_schedule = Schedule.objects.all()

    if request.method == 'POST':
        # Collect data from the submitted form
        owner_name = request.POST.get('ownerName')
        pet_name = request.POST.get('petName')
        pet_species = request.POST.get('petSpecies')
        visit_date = request.POST.get('date')
        reason = request.POST.get('reason')
        diagnosis_text = request.POST.get('diagnosis')
        treatment = request.POST.get('treatment')
        dosage = request.POST.get('dosage')
        follow_up = request.POST.get('followUp')

        # Validate required fields
        required_fields = [
            owner_name, pet_name, pet_species,
            visit_date, reason, diagnosis_text, treatment
        ]
        if not all(required_fields):
            context = {
                'schedule': all_schedule,
                'error': "All fields marked as required must be filled."
            }
            return render(request, 'VetWindow.html', context)

        try:
            # Save the diagnosis to the database
            diagnosis = Diagnosis(
                owner_name=owner_name,
                pet_name=pet_name,
                pet_species=pet_species,
                date_of_visit=visit_date,
                reason_for_visit=reason,
                diagnosis=diagnosis_text,
                treatment=treatment,
                dosage_instructions=dosage,
                follow_up_care=follow_up
            )
            diagnosis.save()

            # Remove the corresponding schedule entry
            Schedule.objects.filter(Name=owner_name).delete()

            # Redirect to avoid duplicate submissions
            return redirect('vet')

        except Exception as e:
            # Handle unexpected errors
            context = {
                'schedule': all_schedule,
                'error': f"An error occurred: {str(e)}"
            }
            return render(request, 'VetWindow.html', context)

    # Render the page with the schedule data
    context = {
        'schedule': all_schedule,
    }
    return render(request, 'VetWindow.html', context)


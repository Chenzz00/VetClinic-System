from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from pytz import timezone as pytz_timezone
from django.db import models
from django.utils import timezone
import pytz
from zoneinfo import ZoneInfo 

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        """
        Create and return a regular user with an email and password.
        """
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)  # Ensures password is hashed
        user.save(using=self._db)
        return user



class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    fname = models.CharField(max_length=30)
    lname = models.CharField(max_length=30)
    number = models.CharField(max_length=15)
    last_login = models.DateTimeField(default=timezone.now)
    
    # Add custom fields for extra info
    is_active = models.BooleanField(default=True)
  
    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['fname', 'lname', 'number']

    def __str__(self):
        return self.email

    def save(self, *args, **kwargs):
        # Set last_login to the current time in Philippine Standard Time (PST)
        if not self.last_login:
            utc_time = datetime.utcnow().replace(tzinfo=ZoneInfo("UTC"))  # Get current UTC time
            # Convert the UTC time to Philippine Standard Time (PST)
            self.last_login = utc_time.astimezone(ZoneInfo("Asia/Manila"))  # Use zoneinfo for conversion
        
        super().save(*args, **kwargs)

class Diagnosis(models.Model):
    owner_name = models.CharField(max_length=100)
    pet_name = models.CharField(max_length=100)
    pet_species = models.CharField(max_length=100)
    date_of_visit = models.DateField()
    reason_for_visit = models.TextField()
    diagnosis = models.TextField()
    treatment = models.TextField()
    dosage_instructions = models.TextField(blank=True, null=True)
    follow_up_care = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Diagnosis for {self.pet_name} on {self.date_of_visit}"

class AvailableSlot(models.Model):
    available_slot_time = models.DateTimeField(unique=True, verbose_name='Available Slot Time')  # Use DateTimeField for better time handling
    slots_left = models.IntegerField(verbose_name='Slots Left')

    def __str__(self):
        return f"Available Time: {self.available_slot_time}, Slots Left: {self.slots_left}"


from datetime import datetime

class Schedule(models.Model):
    account = models.ForeignKey(CustomUser, on_delete=models.CASCADE)  # Link to Accounts
    Name = models.CharField(max_length=100)
    date = models.DateField()
    time = models.CharField(max_length=200)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    services = models.CharField(max_length=100)
    species = models.CharField(max_length=50)
    status = models.CharField(max_length=50, blank=True, null=True)
    payment_status = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        # Format time without a.m./p.m.
        formatted_time = self.time.strftime('%H:%M')  # 24-hour format (e.g., 14:30)
        return f"{self.Name} - {self.date} {formatted_time}"


    
class species(models.Model):
    animal = models.CharField(max_length=30)
   
    def __str__(self):
        return f"{self.animal}"
    
class services(models.Model):
    services = models.CharField(max_length=30)
    amount = models.DecimalField(max_digits=10, decimal_places=2)  # Service amount
   
   
   
    def __str__(self):
        return f"{self.services}"
    


    

class TransactionHistory(models.Model):
    date = models.DateField(verbose_name='Date')
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Amount')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name='User')
    appointment = models.ForeignKey(Schedule, on_delete=models.CASCADE, verbose_name='Appointment')  # Link to Schedule

    @property
    def species(self):
        return self.appointment.species

    @property
    def services(self):
        return self.appointment.services

    def __str__(self):
        return f"User: {self.user.fname} {self.user.lname}, Date: {self.date}, Amount: {self.amount}, Species: {self.species}, Services: {self.services}"


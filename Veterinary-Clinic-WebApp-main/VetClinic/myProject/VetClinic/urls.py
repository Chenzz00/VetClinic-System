from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('logout/', views.logout_view, name='logout'),  
      
    path('registration/', views.registration, name='registration'),  
    path('forgot-password/', views.forgot, name='forgot'),
    path('reset-password/<str:encoded_email>/<str:token>/', views.reset_password, name='reset_password'),
    path('Appointment-Schedule/', views.admin, name='admin'),  
    path('Client-Records/', views.vet, name='vet'),  
    path('Transaction-History/', views.trans, name='trans'),  
    path('Vet-History/', views.vetHistory, name='vetHistory'),
    path('diagnosis/<int:diagnosis_id>/', views.diagnosis_detail, name='diagnosis_detail'),
    path('Change-password/', views.change, name='change'),  
    path('Homepage/', views.owner, name='owner'),  
    path('profile/', views.profile, name='profile'),  
    path('MyHistory/', views.ownhistory, name='ownhistory'), 
    path('Appointment/', views.appwindow, name='appwindow'),  
    path('Admin-History/', views.adhistory, name='adhistory'),  
    path('Account-History/', views.adaccount, name='adaccount'), 
    path('dashboard/', views.dashboard, name='dashboard'), 
     path('email-sent/', views.email_sent, name='email_sent'),
    path('diagnosis/', views.diagnosis, name= 'diagnosis'),
    path('pending-appointment/', views.PendingAppointment, name= 'pAppointment'),
    
]

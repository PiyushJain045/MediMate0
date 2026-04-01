# your_project/app/tasks.py

from celery import shared_task
import smtplib
from django.conf import settings

from .models import Appointment
from datetime import date, timedelta

import smtplib
from email.message import EmailMessage

@shared_task
def send_appointment_reminders():

    print("INSIDE TASK: send_appointment_reminders")

    # Calculate tomorrow's date
    tomorrow = date.today() + timedelta(days=1)
    
    # Filter appointments for tomorrow
    appointments_for_tomorrow = Appointment.objects.filter(date=tomorrow).first()

    if appointments_for_tomorrow == None:
        return f"No appointments for {tomorrow}. Task finished."
    
    print(f"Found {appointments_for_tomorrow}'s appointment for {tomorrow}.")
    
    # Sneder Email Data
    sender_email = settings.EMAIL_HOST_USER
    password = settings.EMAIL_HOST_PASSWORD
    default_from_email = settings.DEFAULT_FROM_EMAIL

    # Receiver email data
    try:
        receiver_email = appointments_for_tomorrow.user.email  # Assuming each appointment has a user with an email field
    except Exception as e:
        print(f"Error retrieving user email: {e}")
        return f"No email found for user {appointments_for_tomorrow.user}"
    
    # Create the email message
    msg = EmailMessage()
    msg["Subject"] = f"Reminder: Your Appointment Tomorrow - '{appointments_for_tomorrow.title}'"
    msg["From"] = default_from_email
    msg["To"] = receiver_email
    msg.set_content(f""" Hello {appointments_for_tomorrow.user.username},

This is a reminder for your upcoming appointment with {appointments_for_tomorrow.title}

Date: {appointments_for_tomorrow.date.strftime('%A, %B %d, %Y')}

We look forward to seeing you.

Sincerely,
The MediMate Team """ )

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()  # Secure the connection
            server.login(sender_email, password)
            server.send_message(msg)
            print("Email sent successfully!")
    except Exception as e:
        print("Error:", e)

        
    return f"Completed sending reminders for {tomorrow}."


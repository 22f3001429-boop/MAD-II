from celery import Celery
from mail import send_mail, send_html_mail, send_mail_with_attachment
from datetime import datetime, timedelta
import os
import csv
import io

celery = Celery('tasks')
celery.conf.update(
    broker_url='redis://localhost:6379/0',
    result_backend='redis://localhost:6379/0',
    task_serializer='json',
    result_serializer='json',
    accept_content=['json'],
    timezone='UTC',
    enable_utc=True,
)

@celery.task(bind=True)
def send_email_task(self, to_email, subject, body):
        result = send_mail(to_email, subject, body)
        if result:
            return f"Email sent successfully to {to_email}"
        else:
            return f"Failed to send email to {to_email}"

@celery.task(bind=True)
def send_html_email_task(self, to_email, subject, html_body):
        result = send_html_mail(to_email, subject, html_body)
        if result:
            return f"HTML email sent successfully to {to_email}"
        else:
            return f"Failed to send HTML email to {to_email}"

@celery.task(bind=True)
def send_reservation_confirmation(self, user_email, reservation_details):
    subject = "Parking Reservation Confirmation - Vehile Parking"
    body = f"""
Dear Customer,

Your parking reservation has been confirmed!

Reservation Details:
- Reservation ID: {reservation_details.get('id', 'N/A')}
- Parking Lot: {reservation_details.get('lot_name', 'N/A')}
- Spot Number: {reservation_details.get('spot_number', 'N/A')}
- Start Time: {reservation_details.get('start_time', 'N/A')}
- End Time: {reservation_details.get('end_time', 'N/A')}
- Total Amount: ₹{reservation_details.get('total_amount', 'N/A')}

Thank you for choosing Vehile Parking!

Best regards,
Vehile Parking Team
    """
    
    return send_email_task.delay(user_email, subject, body)

@celery.task(bind=True)
def send_reservation_reminder(self, user_email, reservation_details):
    subject = "Parking Reservation Reminder - Vehile Parking"
    body = f"""
Dear Customer,

This is a reminder that your parking reservation is starting soon!

Reservation Details:
- Reservation ID: {reservation_details.get('id', 'N/A')}
- Parking Lot: {reservation_details.get('lot_name', 'N/A')}
- Spot Number: {reservation_details.get('spot_number', 'N/A')}
- Start Time: {reservation_details.get('start_time', 'N/A')}
- End Time: {reservation_details.get('end_time', 'N/A')}

Please arrive on time to secure your parking spot.

Best regards,
Vehile Parking Team
    """
    
    return send_email_task.delay(user_email, subject, body)

@celery.task(bind=True)
def send_welcome_email(self, user_email, username):
    subject = "Welcome to Vehile Parking!"
    body = f"""
Dear {username},

Welcome to Vehile Parking! 

Your account has been successfully created. You can now:
- Search for parking spots
- Make reservations
- Manage your bookings
- View your parking history

Thank you for choosing Vehile Parking for your parking needs!

Best regards,
Vehile Parking Team
    """
    
    return send_email_task.delay(user_email, subject, body)

@celery.task(bind=True)
def send_cancellation_email(self, user_email, reservation_details):
    subject = "Parking Reservation Cancelled - Vehile Parking"
    body = f"""
Dear Customer,

Your parking reservation has been cancelled.

Cancelled Reservation Details:
- Reservation ID: {reservation_details.get('id', 'N/A')}
- Parking Lot: {reservation_details.get('lot_name', 'N/A')}
- Spot Number: {reservation_details.get('spot_number', 'N/A')}
- Start Time: {reservation_details.get('start_time', 'N/A')}
- End Time: {reservation_details.get('end_time', 'N/A')}

If you have any questions, please contact our support team.

Best regards,
Vehile Parking Team
    """
    
    return send_email_task.delay(user_email, subject, body)

# Periodic tasks setup
from celery.schedules import crontab

celery.conf.beat_schedule = {
    'send-test-email': {
        'task': 'tasks.send_email_task',
        'schedule': crontab(minute='*/30'), 
        'args': ('test@example.com', 'Test Email', 'This is a test email from Celery')
    },
}


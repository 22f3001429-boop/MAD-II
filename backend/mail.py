import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import os
from dotenv import load_dotenv

load_dotenv()

SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT =  587
EMAIL_ADDRESS ='my-email@gmail.com'
EMAIL_PASSWORD = 'password'

def send_mail(to_email, subject, body):
    try:
        msg = MIMEMultipart()
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = to_email
        msg['Subject'] = subject
        
        msg.attach(MIMEText(body, 'plain'))
        
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        
        if EMAIL_PASSWORD:
            server.starttls() 
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        
        text = msg.as_string()
        server.sendmail(EMAIL_ADDRESS, to_email, text)
        server.quit()
        
        print(f"Email sent successfully to {to_email}")
        return True
        
    except Exception as e:
        print(f"Error sending email to {to_email}: {str(e)}")
        return False

def send_html_mail(to_email, subject, html_body):
    try:
        msg = MIMEMultipart('alternative')
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = to_email
        msg['Subject'] = subject
        
        html_part = MIMEText(html_body, 'html')
        msg.attach(html_part)
        
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        
        if EMAIL_PASSWORD:
            server.starttls()  
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        
        text = msg.as_string()
        server.sendmail(EMAIL_ADDRESS, to_email, text)
        server.quit()
        
        print(f"HTML email sent successfully to {to_email}")
        return True
        
    except Exception as e:
        print(f"Error sending HTML email to {to_email}: {str(e)}")
        return False

def send_bulk_mail(email_list, subject, body):
    success_count = 0
    for email in email_list:
        if send_mail(email, subject, body):
            success_count += 1
    
    print(f"Bulk email sent: {success_count}/{len(email_list)} successful")
    return success_count

def send_mail_with_attachment(to_email, subject, body, attachment_path, attachment_name=None):
    """Send email with file attachment"""
    try:
        msg = MIMEMultipart()
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = to_email
        msg['Subject'] = subject
        
        # Add body to email
        msg.attach(MIMEText(body, 'plain'))
        
        # Add attachment
        if os.path.exists(attachment_path):
            with open(attachment_path, "rb") as attachment:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(attachment.read())
            
            encoders.encode_base64(part)
            
            # Set attachment filename
            filename = attachment_name or os.path.basename(attachment_path)
            part.add_header(
                'Content-Disposition',
                f'attachment; filename= {filename}',
            )
            
            msg.attach(part)
        else:
            print(f"Attachment file not found: {attachment_path}")
            return False
        
        # Send email
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        
        if EMAIL_PASSWORD:
            server.starttls()
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        
        text = msg.as_string()
        server.sendmail(EMAIL_ADDRESS, to_email, text)
        server.quit()
        
        print(f"Email with attachment sent successfully to {to_email}")
        return True
        
    except Exception as e:
        print(f"Error sending email with attachment to {to_email}: {str(e)}")
        return False
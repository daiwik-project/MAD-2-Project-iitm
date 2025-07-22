# controllers\admin\auth.py

import random
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from flask import current_app, render_template
from models.model import Admin, db


def find_admin(email):
    admin = Admin.query.filter_by(admin_email=email).first()
    return admin


def send_otp_for_admin(admin_object):

    try:

        otp_code = str(random.randint(100000, 999999))
        print(f"Generated OTP {otp_code} for admin {admin_object.admin_email}")

        admin_object.admin_token = otp_code
        db.session.commit()
        print(f"Successfully saved OTP to the database for {admin_object.admin_email}.")

        msg = MIMEMultipart()
        msg['From'] = current_app.config['MAIL_USERNAME']
        msg['To'] = admin_object.admin_email 
        msg['Subject'] = 'Your Admin Login OTP'

        html_body = render_template('admin_otp.html', otp=otp_code)
        msg.attach(MIMEText(html_body, 'html'))

        print(f"Connecting to Gmail to send OTP to {admin_object.admin_email}...")
        with smtplib.SMTP(current_app.config['MAIL_SERVER'], current_app.config['MAIL_PORT']) as server:
            server.starttls()
            server.login(current_app.config['MAIL_USERNAME'], current_app.config['MAIL_PASSWORD'])
            server.send_message(msg)

        print(f"SUCCESS: OTP Email sent successfully to {admin_object.admin_email}!")
        return True

    except Exception as e:
        db.session.rollback()
        print(f"FATAL ERROR: Could not send OTP email. Reason: {e}")
        return False



def actual_otp(email):
    admin = Admin.query.filter_by(admin_email=email).first()
    if admin:
        return admin.admin_token
    else:
        return None
    

def  check_n_add_admin():
    if Admin.query.first() is None:
        print("="*25)
        print("DATABASE SETUP: No admin found. Creating a default admin.")
        default_email = "devproject2024@gmail.com"
        default_admin = Admin(
                    admin_email=default_email,
                    admin_token="password" 
                )
        db.session.add(default_admin)
        db.session.commit()
        print("Default admin created successfully!")
        print(f"  -> Email: {default_email}")
        print(f"  -> TEMPORARY PASSWORD: password")
        print("Please use this password for your first login and change it.")

    else:
        print("INFO: Admin(s) already exist in the database. No action taken.")


   
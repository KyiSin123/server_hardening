#!/usr/bin/python3

import os
import requests
import smtplib
from email.mime.text import MIMEText

# Get the last SSH login IP from auth.log
def get_last_login_ip():
    try:
        log_output = os.popen("tail -n 20 /var/log/auth.log | grep 'Accepted' | tail -n 1").read()
        ip = log_output.split(" ")[10]  # Extract IP from log line
        return ip
    except IndexError:
        return None

# Get location details using ipinfo.io
def get_ip_location(ip):
    try:
        response = requests.get(f"https://ipinfo.io/{ip}/json")
        data = response.json()
        return data.get("city", "Unknown"), data.get("country", "Unknown")
    except Exception as e:
        return "Error", "Error"

# Send an email alert
def send_alert(ip, city, country):
    sender_email = "kyisinshoon5101998@gmail.com"
    receiver_email = "kyisinshoonlaelinn@gmail.com"
    subject = "🔴 SSH Login Alert!"
    body = f"Unusual SSH login detected!\n\nIP: {ip}\nLocation: {city}, {country}\n"

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = receiver_email

    # Configure your email SMTP server (Gmail example)
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_email, "svwfebnsepiljogt")
        server.sendmail(sender_email, receiver_email, msg.as_string())
        server.quit()
    except Exception as e:
        print("Failed to send email:", e)

# Run the detection
if __name__ == "__main__":
    usual_city = "Yangon"

    ip = get_last_login_ip()
    if ip:
        city, country = get_ip_location(ip)
        print(f"Login from {city}, {country} (IP: {ip})")

        # If login is from an unusual city, send an alert
        if city != usual_city:
            print('alert')
            send_alert(ip, city, country)
    else:
        print("No recent SSH login detected.")

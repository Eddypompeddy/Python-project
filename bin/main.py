krimport requests
import difflib
import smtplib
from email.mime.text import MIMEText

def get_website_content(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        else:
            return None
    except requests.RequestException as e:
        print("Fehler beim Abrufen der Website:", e)
        return None

def send_email(content_diff):
    sender_email = 'edgarkrapp.ek@gmail.com' # Deine E-Mail-Adresse
    receiver_email = 'edgarkrapp.ek@gmail.com' # Empfänger-E-Mail-Adresse
    password = 'Seelsorge1+' # Dein E-Mail-Passwort

    subject = 'Website aktualisiert!'
    body = f'Die Website wurde aktualisiert. Änderungen:\n\n{content_diff}'

    message = MIMEText(body)
    message['Subject'] = subject
    message['From'] = sender_email
    message['To'] = receiver_email

    try:
        server = smtplib.SMTP_SSL('smtp.example.com', 465) # SMTP-Server und Port eintragen
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message.as_string())
        server.quit()
        print("E-Mail gesendet!")
    except smtplib.SMTPException as e:
        print("Fehler beim Senden der E-Mail:", e)

def check_website(url):
    content = get_website_content(url)
    if content:
        with open('previous_content.txt', 'r+') as file:
            previous_content = file.read()
            if previous_content:
                d = difflib.Differ()
                diff = list(d.compare(previous_content.splitlines(), content.splitlines()))
                if any(line.startswith('+') or line.startswith('-') for line in diff):
                    send_email('\n'.join(diff))
            file.seek(0)
            file.truncate()
            file.write(content)

# Beispielaufruf: Überwachung einer Website alle 30 Minuten
url_to_monitor = 'https://example.com' # URL der zu überwachenden Website

while True:
    check_website(url_to_monitor)
    time.sleep(3600) # Überprüfe alle 30 Minuten (Anpassung der Überprüfungsintervalle nach Bedarf)

    

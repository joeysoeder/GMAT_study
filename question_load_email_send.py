import smtplib
from email.mime.text import MIMEText
import random
import os
import sys

# Configuration
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587  
EMAIL_ADDRESS = os.environ.get('EMAIL_ADDRESS')
EMAIL_PASSWORD = os.environ.get('EMAIL_PASSWORD')
RECIPIENT_EMAILS = os.environ.get('RECIPIENT_EMAILS', '').split(',') 
QUESTIONS_FILE = 'GMAT_Quant_Questions.txt'
SENT_QUESTIONS_FILE = 'sent_questions.txt'

def load_questions():
    with open(QUESTIONS_FILE, 'r', encoding='utf-8') as f:
        questions = f.read().split('\n\n') 
    return questions

def load_sent_questions():
    if os.path.exists(SENT_QUESTIONS_FILE):
        with open(SENT_QUESTIONS_FILE, 'r', encoding='utf-8') as f:
            sent_questions = set(f.read().splitlines())
    else:
        sent_questions = set()
    return sent_questions

def save_sent_question(question):
    with open(SENT_QUESTIONS_FILE, 'a', encoding='utf-8') as f:
        f.write(question.strip() + '\n')

def choose_question(questions, sent_questions):
    remaining_questions = [q for q in questions if q.strip() not in sent_questions]
    if not remaining_questions:
        print("All questions have been sent.")
        sys.exit()
    question = random.choice(remaining_questions)
    return question.strip()

def send_email(subject, body):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = ', '.join(RECIPIENT_EMAILS)

    server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    server.starttls()
    server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
    server.sendmail(EMAIL_ADDRESS, RECIPIENT_EMAIL, msg.as_string())
    server.quit()

def main():
    if not EMAIL_PASSWORD:
        print("Email password not set. Please set the EMAIL_PASSWORD environment variable.")
        sys.exit(1)

    questions = load_questions()
    sent_questions = load_sent_questions()
    question = choose_question(questions, sent_questions)
    subject = 'Your Daily GMAT Quant Question'
    body = question

    send_email(subject, body)
    save_sent_question(question)
    print("Email sent successfully.")

if __name__ == '__main__':
    main()

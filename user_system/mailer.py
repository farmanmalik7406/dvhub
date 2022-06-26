import math
import random
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class OtpGen:
    def __init__(self):
        self.otp = self.generate()

    def generate(self):
        otp = ""
        digits = "".join(str(x) for x in range(0, 10))
        for i in range(6):
            otp += digits[math.floor(random.random() * 10)]
        return otp

    def get_otp(self):
        return self.otp

    def gen_otp(self):
        self.otp = self.generate()


class Mailer(OtpGen):
    def __init__(self):
        super(Mailer, self).__init__()
        self.sender = 'dvhubportal@gmail.com'
        self.pas = 'CrhcFKSJDEQVjHGU'
        self.rec = None
        self.message = MIMEMultipart()
        self.invoked = False
        self.verified = False

    def set_reciever(self, reciever):
        self.rec = reciever

    def send_otp(self):
        self.invoked = True
        self.verified = False
        otp = self.otp
        self.message['From'] = self.sender
        self.message['To'] = self.rec
        self.message['subject'] = "Email Verification for account"
        mail_content = f"""
        this is a account confirmation mail and yout otp is {otp}.
        please enter the same to verify your account
        thanks and regards
        DVHUB
        """
        self.message.attach(MIMEText(mail_content, 'plain'))
        session = smtplib.SMTP('smtp-relay.sendinblue.com', 587)
        session.starttls()
        session.login(self.sender, self.pas)
        text = self.message.as_string()
        session.sendmail(self.sender, self.rec, text)
        session.quit()
        print(self.rec)
        print(self.otp)
        print("sent")

    def verify_otp(self, otp):
        if self.otp == otp:
            self.verified = True
            return True
        return False

    def end(self):
        self.otp = None
        self.invoked = False
        self.verified = False

import smtplib
from abc import ABC, abstractmethod
from email.mime.text import MIMEText


class Notifier(ABC):
    @abstractmethod
    def send_noti(sender_addr: str, to_addr: str, body: str):
        pass


class EmailNotifier():
    """
    This class is for sending the email notification
    """

    def __init__(self) -> None:
        self.sender_addr = "ams.ltd100@gmail.com"
        self.password = "erpyvkvpxmqjrzfc"

    def send_noti(self, to_addr: str, body: str):
        """This function sends the notification as email

        Args:
            to_addr (str): Email address of the reciever
            body (str): Body of the email
        """
        msg = MIMEText(body)
        msg["Subject"] = "Changed Password"
        msg["From"] = self.sender_addr
        msg["To"] = to_addr
        with smtplib.SMTP("smtp.gmail.com", 587) as smtp_server:
            smtp_server.ehlo("Gmail")
            smtp_server.starttls()
            smtp_server.login(self.sender_addr, self.password)
            smtp_server.sendmail(self.sender_addr, [to_addr], msg.as_string())
        print("Email Sent !!")


emailNotifier = EmailNotifier()

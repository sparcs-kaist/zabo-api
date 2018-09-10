from django.core.mail import send_mail

class MailHelpers():

    def __init__(self, zaboMail):
        self.zaboMail = zaboMail

    def sendMail(self):
        send_mail(
            self.zaboMail.subject,
            self.zaboMail.message,
            self.zaboMail.sender_address,
            self.zaboMail.get_receivers_addresss(),
            fail_silently=False,
        )
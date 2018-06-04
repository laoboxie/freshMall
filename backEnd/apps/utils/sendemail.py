from django.core.mail import send_mail
from backEnd.settings import EMAIL_HOST_USER


sms_email_template = "[生鲜电商]您的短信验证码是：{code}"


class SendEmail(object):
    def __init__(self):
        pass

    def send_smscode_email(self, code, email_addr ):
        return send_mail(
            "生鲜电商——短信验证码",
            sms_email_template.format(code=code),
            EMAIL_HOST_USER,
            [email_addr],
            fail_silently=False,
        )




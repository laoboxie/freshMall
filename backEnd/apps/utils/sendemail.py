from django.core.mail import send_mail
from backEnd.settings import DEFAULT_FROM_EMAIL


sms_email_template = "[生鲜电商]您的短信验证码是：{code}"


class SendSmsEmail(object):
    def __init__(self):
        pass

    def send_email(self, code, email_addr, ):
        send_mail(
            "生鲜电商——短信验证码",
            sms_email_template.format(code=code),
            DEFAULT_FROM_EMAIL,
            [].append(email_addr),
            fail_silently=False,
        )


email = SendSmsEmail()
email.send_email("1234", "594502135@qq.com")



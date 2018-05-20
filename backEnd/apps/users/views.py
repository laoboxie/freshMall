from django.shortcuts import render
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q
from rest_framework.mixins import CreateModelMixin
from rest_framework import mixins, viewsets, status
from rest_framework.response import Response
from random import choice

from apps.utils.sendemail import SendSmsEmail
from .models import VerifyCode
from .serializers import SmsCodeSerializer
# Create your views here.
User = get_user_model()


class CustomBackend(ModelBackend):
    """
    自定义用户验证
    """
    def authenticate(self, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(Q(username=username) | Q(mobile=username) | Q(email=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None


class SmsCodeViewset(CreateModelMixin, viewsets.GenericViewSet):
    """
    发送邮件验证码
    """
    serializer_class = SmsCodeSerializer

    def generate_code(self):
        code_nums = 4
        seeds = "0123456789"
        random_result = []
        for a in range(code_nums):
            random_result.append(choice(seeds))
        return "".join(random_result)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        account = serializer.validated_data["account"]
        email = SendSmsEmail()
        code = self.generate_code()
        send_status = email.send_email(code, account)
        if send_status == 0:
            return Response({
                "account": "发送验证码失败"
            }, status=status.HTTP_400_BAD_REQUEST)
        else:
            code_record = VerifyCode(code=code, account=account)
            code_record.save()
            return Response({
                "account": account
            }, status=status.HTTP_201_CREATED)




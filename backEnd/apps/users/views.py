from django.shortcuts import render
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q
from rest_framework.mixins import CreateModelMixin
from rest_framework import mixins, viewsets, status
from rest_framework.response import Response
from random import choice
from rest_framework_jwt.serializers import jwt_encode_handler, jwt_payload_handler

from apps.utils.sendemail import SendEmail
from .models import VerifyCode
from .serializers import SmsCodeSerializer, UserRegSerializer
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
        email_ins = SendEmail()
        code = self.generate_code()
        send_status = email_ins.send_smscode_email(code, account)
        if send_status == 0:
            return Response({
                "account": "发送验证码失败"
            }, status=status.HTTP_400_BAD_REQUEST)
        else:
            account_record = VerifyCode.objects.filter(account=account)
            if account_record.count():
                account_record.delete()

            code_record = VerifyCode(code=code, account=account)
            code_record.save()
            return Response({
                "account": account
            }, status=status.HTTP_201_CREATED)


class UserRegViewset(CreateModelMixin, viewsets.GenericViewSet):
    """
    用户注册
    """
    serializer_class = UserRegSerializer
    queryset = User.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.perform_create(serializer)

        re_dict = serializer.data
        payload = jwt_payload_handler(user)
        re_dict["token"] = jwt_encode_handler(payload)
        re_dict["name"] = user.name if user.name else user.username

        headers = self.get_success_headers(serializer.data)
        return Response(re_dict, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        return serializer.save()








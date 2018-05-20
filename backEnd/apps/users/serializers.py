from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.validators import UniqueValidator
from apps.utils.regexp import EMAIL_REG
import re
from datetime import datetime, timedelta
from .models import VerifyCode

User = get_user_model()


class SmsCodeSerializer(serializers.Serializer):
    account = serializers.CharField(max_length=100)

    def validate_account(self, account):
        """
        验证帐号
        :param account:
        :return:
        """
        # 手机是否注册
        if User.objects.filter(email=account).count():
            raise serializers.ValidationError("帐号已被注册")
        # 帐号是否合法
        if not re.match(EMAIL_REG, account):
            raise serializers.ValidationError("帐号格式不正确")
        # 验证码发送频率
        frequency = timedelta(seconds=30)
        latest_datetime = datetime.now() - frequency
        if VerifyCode.objects.filter(add_time__gt=latest_datetime, account=account).count():
            raise serializers.ValidationError("发送频率过快，请稍后重试")

        return account
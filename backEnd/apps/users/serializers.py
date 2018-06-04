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


class UserRegSerializer(serializers.ModelSerializer):
    code = serializers.CharField(required=True, min_length=4, max_length=6, label="验证码", write_only=True,
                                 error_messages={
                                     "blank": "请输入验证码",
                                     "required": "请输入验证码",
                                     "max_length": "验证码格式错误",
                                     "min_length": "验证码格式错误"
                                 })

    password = serializers.CharField(style={'input_type': 'password'}, label="密码", write_only=True)

    class Meta:
        model = User
        fields = ("username", "code", "password")

    # def create(self, validated_data):
    #     user = super(UserRegSerializer, self).create(validated_data=validated_data)
    #     user.set_password(validated_data["password"])
    #     user.save()
    #     return user

    def validate_code(self, code):
        verify_records = VerifyCode.objects.filter(account=self.initial_data["username"])\
                        .order_by("-add_time")
        if verify_records.count():
            last_record = verify_records[0]
            validate_time = timedelta(minutes=5)
            if datetime.now()-last_record.add_time>validate_time:
                raise serializers.ValidationError("验证码已过期")

            if last_record.code != code:
                raise serializers.ValidationError("验证码错误")
        else:
            raise serializers.ValidationError("请先获取验证码")

        return code

    def validate(self, attrs):
        attrs["email"] = attrs["username"]
        del attrs["code"]
        return attrs



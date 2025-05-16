from rest_framework import serializers
from api.models import *
from django.contrib.auth.password_validation import validate_password #hàm kiểm tra  độ mạnh của mật khẩu


class RegisterSerializers(serializers.ModelSerializer):
    password1 = serializers.CharField(write_only = True , validators = [validate_password])
    password2 = serializers.CharField(write_only = True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2','phone']

    def validate (self , data):
        if data['password1'] != data['password2']:
            raise serializers.ValidationError("Không đúng mật khẩu")
        
        if User.objects.filter(username=data['username']).exists():
            raise serializers.ValidationError("Tên người dùng đã tồn tại")

        if User.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError("Email đã được đăng ký")
    
        return data
    def create(self, validated_data):
        password = validated_data.pop('password1')#lấy mật khẩu thực sự
        validated_data.pop('password2')
        user = User(**validated_data)
        user.set_password(password)  # Hash mật khẩu
        user.save()
        return user

class LoginSerializers(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only = True)

class ResetPassWordSerializers(serializers.Serializer):
    username = serializers.CharField()
    email_or_phone = serializers.CharField()
    new_password1 = serializers.CharField(write_only = True , validators = [validate_password])
    new_password2 = serializers.CharField(write_only = True)
    
    def validate(self , data):
        if data['new_password1'] != data['new_password2'] :
            raise serializers.ValidationError("không trùng mật khẩu")
        
        try:
            user = User.objects.get(username = data['username'])
        except User.DoesNotExist:
            raise serializers.ValidationError("Tài khoản không tồn tại")
        
        if data['email_or_phone'] not in user.email:
            raise serializers.ValidationError("Tên email hoặc số diện thoại không tồn tại")
        
        data['user'] = user 
        return data
            
    def save(self, validated_data):
        user = self.validated_data['user']
        password = validated_data.pop('new_password1')#lấy mật khẩu thực sự
        user.set_password(password)  # Hash mật khẩu
        user.save()
        return user


class CategorySerializers(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'description']
        
from rest_framework import serializers
from .models import Product

class ProductSerializers(serializers.ModelSerializer):
    category_name = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'image', 'category', 'category_name']

    def get_category_name(self, obj):
        return obj.category.name if obj.category else None
    
from django.contrib.auth.models import User
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = 'url','id','first_name','last_name','password','last_login','username','email','date_joined'

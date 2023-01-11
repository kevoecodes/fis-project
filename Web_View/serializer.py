from django.contrib.auth.models import User
from rest_framework import serializers
from Fields_Management.models import Student


class NewStudent(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('password', 'username', 'first_name', 'email')
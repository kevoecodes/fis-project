from django.contrib.auth.models import User
from rest_framework import serializers
from Fields_Management.models import Student, StudentList, StudentApplication


class NewStudent(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('password', 'username', 'first_name', 'email')


class StudentListSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentList
        fields = "__all__"


class StudentApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentApplication
        fields = "__all__"

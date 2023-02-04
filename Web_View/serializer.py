from django import forms
from django.contrib.auth.models import User
from rest_framework import serializers
from Fields_Management.models import Student, StudentList, StudentApplication, Field, CourseField, FieldImage, Course


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


class FieldSerializer(forms.ModelForm):
    class Meta:
        model = Field
        fields = "__all__"


class CourseFieldSerializer(forms.ModelForm):
    class Meta:
        model = CourseField
        fields = "__all__"


class FieldImageForm(forms.ModelForm):
    class Meta:
        model = FieldImage
        fields = "__all__"


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = "__all__"

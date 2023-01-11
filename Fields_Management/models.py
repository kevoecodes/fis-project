from django.conf import settings
from django.db import models


class Course(models.Model):
    name = models.CharField(max_length=200, null=False)

    def __str__(self):
        return self.name


class Student(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.sername


class Field(models.Model):
    company_name = models.CharField(max_length=200, null=False)
    phone = models.CharField(max_length=200, null=False)
    email = models.EmailField(null=False)
    location = models.CharField(max_length=200, null=False)
    meta_details = models.TextField(max_length=500, null=False)
    details = models.TextField(max_length=1000, null=False)

    def __str__(self):
        return self.company_name


class StudentList(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    field = models.ForeignKey(Field, on_delete=models.CASCADE)


class FieldImage(models.Model):
    field = models.ForeignKey(Field, on_delete=models.CASCADE)
    image = models.FileField()

    def __str__(self):
        return self.image.name


class CourseField(models.Model):
    field = models.ForeignKey(Field, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    def __str__(self):
        return self.field.company_name + ' ' + self.course.name


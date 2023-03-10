from django.conf import settings
from django.db import models


class Course(models.Model):
    name = models.CharField(max_length=200, null=False)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return self.name


class Student(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return self.user.username


class Field(models.Model):
    company_name = models.CharField(max_length=200, null=False)
    phone = models.CharField(max_length=200, null=False)
    email = models.EmailField(null=False)
    location = models.CharField(max_length=200, null=False)
    meta_details = models.TextField(max_length=500, null=False)
    details = models.TextField(max_length=1000, null=False)
    open = models.BooleanField(default=True)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return self.company_name


class StudentList(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    field = models.ForeignKey(Field, on_delete=models.CASCADE)

    class Meta:
        ordering = ['-id']


class FieldImage(models.Model):
    title = models.CharField(max_length=200, null=False)
    field = models.ForeignKey(Field, on_delete=models.CASCADE)
    image = models.FileField()

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return self.title + " " + self.image.name


class CourseField(models.Model):
    field = models.ForeignKey(Field, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    def __str__(self):
        return self.field.company_name + ' ' + self.course.name

    class Meta:
        ordering = ['-id']


class StudentApplication(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    field = models.ForeignKey(Field, on_delete=models.CASCADE)
    file = models.FileField()

    PENDING = 0
    ACCEPTED = 1
    DECLINED = 2
    STATUSES = (
        (PENDING, 'Pending Application'),
        (ACCEPTED, 'Accepted Application'),
        (DECLINED, 'Declined Application')
    )
    status = models.IntegerField(choices=STATUSES, default=PENDING)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    class Meta:
        ordering = ['-id']

from django.db import models


class Course(models.Model):
    name = models.CharField(max_length=200, null=False)

    def __str__(self):
        return self.name


class Field(models.Model):
    company_name = models.CharField(max_length=200, null=False)
    phone = models.CharField(max_length=200, null=False)
    email = models.EmailField(null=False)
    location = models.CharField(max_length=200, null=False)
    meata_details = models.TextField(max_length=500, null=False)
    details = models.TextField(max_length=500, null=False)

    def __str__(self):
        return self.company_name


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


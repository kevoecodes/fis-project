from django.contrib import admin

# Register your models here.
from .models import *

_ = [Field, Course, CourseField, FieldImage, Student, StudentList, StudentApplication
     ]

for i in _:
    admin.site.register(i)

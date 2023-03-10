import json
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.models import User
from Fields_Management.models import Field, Course, Student, StudentList, FieldImage, CourseField, StudentApplication
from Web_View.form import StudentApplicationForm
from Web_View.serializer import NewStudent, StudentListSerializer, StudentApplicationSerializer, FieldSerializer, \
    CourseFieldSerializer, FieldImageForm, CourseForm


def studentRegistration(request):
    if request.method == "POST":
        print(request.POST)
        data = request.POST
        form = NewStudent(data=request.POST)
        if form.is_valid():
            new_user = User()
            new_user.set_password(data['password'])
            new_user.username = data['username']
            new_user.first_name = data['first_name']
            new_user.email = data['email']
            new_user.save()

            new_student = Student()
            new_student.course = Course.objects.get(id=data['course'])
            new_student.user = new_user
            new_student.save()

            return redirect('/login')
        messages.error(request, "Check for redundant data or too short password")
        return redirect('/register')

    courses = Course.objects.all()
    return render(request, 'register.html', {"courses": courses})


def studentLogin(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect("/")
            else:
                messages.error(request, "Invalid username or password.")
                return redirect('/login')
        else:
            messages.error(request, "Invalid username or password.")
            return redirect('/login')

    if request.method == "GET":
        return render(request, 'login.html')


def index(request):
    if request.user.is_authenticated:
        course_fields = CourseField.objects.all()
        student = None
        id = None
        try:
            student = Student.objects.get(user_id=request.user.id)
            id = student.id
            course_fields = course_fields.filter(course_id=student.course.id)
        except Student.DoesNotExist as e:
            pass
        fields = []
        field_ids = []
        for i in course_fields:
            is_fav = False
            applied = False
            if student is not None:
                try:
                    applied_ = StudentApplication.objects.get(student_id=student.id, field_id=i.field.id)
                    if applied_ is not None:
                        print('Field applied')
                        applied = True
                except StudentApplication.DoesNotExist as e:
                    print("Not Appleieddddd")
                    pass
                try:
                    fav = StudentList.objects.get(field_id=i.field.id, student_id=student.id)
                    if fav is not None:
                        is_fav = True
                except StudentList.DoesNotExist as e:
                    pass

            print(is_fav)
            fields.append({
                "id": i.field.id,
                "company_name": i.field.company_name,
                "phone": i.field.phone,
                "meta_details": i.field.meta_details,
                "is_fav": is_fav,
                "applied": applied
            })
            field_ids.append(i.field.id)
        return render(request, 'index.html', {
            "fields": fields,
            "field_ids": json.dumps(list(field_ids)),
            "length": len(fields),
            "student_id": id
        })

    return redirect('/login')


def moreDetails(request, pk):
    if request.user.is_authenticated:
        try:
            field = Field.objects.get(id=pk)
            images = []
            _images = FieldImage.objects.filter(field_id=field.id)
            print(_images)
            for i in range(0, len(_images)):
                print(i)
                data = dict({
                    "title": _images[i].title,
                    "class": "carousel-item",
                    "image": _images[i].image,
                })
                print(_images[i].image.url)
                if i == 0:
                    data['class'] = "carousel-item active"
                images.append(data)
            return render(
                request, 'more_details.html', {"field": field, "images": images}
            )
        except Field.DoesNotExist as e:
            print(e)
            return redirect('/')

    return redirect('/login')


def myList(request):
    if request.user.is_authenticated:
        _fields = []
        try:
            student = Student.objects.get(user_id=request.user.id)
            fields = Field.objects.all()
            for field in fields:
                status = 33
                applied = False
                is_fav = False
                try:
                    stapplied = StudentApplication.objects.get(student_id=student.id, field_id=field.id)
                    if stapplied is not None:
                        applied = True
                        status = stapplied.status
                except StudentApplication.DoesNotExist as e:
                    print(e)
                    pass
                try:
                    stlist = StudentList.objects.get(student_id=student.id, field_id=field.id)
                    if stlist is not None:
                        print("Is Fave")
                        is_fav = True
                except StudentList.DoesNotExist as e:
                    print(e)
                    pass
                if is_fav or applied:
                    print("is")
                    _fields.append({
                        "id": field.id,
                        "is_fav": is_fav,
                        "applied": applied,
                        "status": status,
                        "company_name": field.company_name,
                        "meta_details": field.meta_details,
                    })
        except Student.DoesNotExist:
            pass
        return render(request, 'mylist.html', {"fields": _fields, "length": len(_fields)})

    return redirect('/login')


def Logout(request):
    logout(request)
    return redirect('/login')


class MyListManager(APIView):
    permission_classes = [AllowAny]

    @staticmethod
    def post(request, *args, **kwargs):
        data = request.data
        if data['status'] == "1":
            serializer = StudentListSerializer(data={
                "field": data["field_id"],
                "student": data["student_id"]
            })
            if serializer.is_valid():
                print("Serializer")
                serializer.save()
        else:
            try:
                stl = StudentList.objects.get(
                    field_id=data["field_id"],
                    student_id=data["student_id"]
                )
                stl.delete()
            except StudentList.DoesNotExist:
                pass
        return Response(True)


def student_application(request, pk):
    if request.user.is_authenticated:
        if request.method == "POST":
            print(request.POST)

            print(request.FILES)
            serializer = StudentApplicationForm(request.POST, request.FILES)
            if serializer.is_valid():
                serializer.save()
                messages.success(request, "Successfully Applied")
                print("Success")
            else:
                print(serializer.errors)
                messages.error(request, serializer.errors)
            return redirect('/')
        elif request.method == "GET":
            try:
                field = Field.objects.get(id=pk)
                student = Student.objects.get(user_id=request.user.id)
                return render(request, 'application.html', {"field": field, "student_id": student.id})
            except (Field.DoesNotExist, Student.DoesNotExist):
                return redirect('/')

        return redirect('/')
    return redirect('/login')


def add_field(request):
    if request.user.is_authenticated and request.user.is_staff:
        if request.method == "POST":
            print(request.POST)
            print(request.FILES['image_1'])
            register_field = RegisterField(data=request.POST, files=request.FILES)
            print(register_field.status, register_field.errors, register_field.stage)
            if register_field.status:
                return redirect('/')
            else:
                return redirect('/add-field')
            # return redirect('/add-field')

        elif request.method == "GET":
            courses = Course.objects.all()
            return render(request, 'add_field.html', {"courses": courses})

    return redirect('/login')


def addCourse(request):
    if request.user.is_authenticated and request.user.is_staff:
        if request.method == "POST":

            form = CourseForm(data=request.POST)
            if form.is_valid():
                form.save()
                return redirect('/')
            return redirect('/add-course')

        elif request.method == "GET":
            return render(request, 'add_course.html', )

    return redirect('/')


def view_applications(request, pk=None):
    if request.user.is_authenticated and request.user.is_staff:
        if request.method == "GET":
            applications = StudentApplication.objects.all()
            if pk is not None:
                applications = applications.filter(field_id=pk)
            return render(request, 'view_applications.html', {"applications": applications})

    return redirect('/login')


def application_approval(request, pk=None):
    if request.user.is_authenticated and request.user.is_staff and pk is not None:
        if request.method == "GET":
            print(pk)
            status = request.GET.get('s', None)
            print(status)
            if status is not None:
                try:
                    application = StudentApplication.objects.get(id=pk)
                    application.status = status
                    application.save()
                except StudentApplication.DoesNotExist:
                    pass
            return redirect('/applications')

    return redirect('/login')


class RegisterField:
    def __init__(self, data, files):
        self.stage = 0
        self.field_id = None
        self.data = data
        self.files = files
        self.field = None
        self.status = True
        self.errors = None

        self.addField()
        if self.status:
            self.addCourseField()
        if self.status:
            self.addFieldImage()

    def addField(self):
        serializer = FieldSerializer(data=self.data)
        if serializer.is_valid():
            self.field = serializer.save()
            self.field_id = self.field.id
            return True
        self.stage = 1
        self.status = False
        self.errors = serializer.errors
        return False

    def addCourseField(self):
        serializer = CourseFieldSerializer(data={
            "field": self.field_id,
            "course": self.data['course']
        })
        if serializer.is_valid():
            serializer.save()
            return True
        self.stage = 2
        self.status = False
        self.errors = serializer.errors
        return False

    def addFieldImage(self):
        try:

            field_image = FieldImage.objects.create(
                field=self.field,
                image=self.files['image_1'],
                title=self.data['title_1']
            )
            field_image.save()

            field_image = FieldImage.objects.create(
                field=self.field,
                image=self.files['image_2'],
                title=self.data['title_2']
            )
            field_image.save()
            pass
        except Exception as e:
            self.stage = 3
            self.status = False
            self.errors = e

        return True

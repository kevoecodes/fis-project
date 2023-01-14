from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.models import User
from Fields_Management.models import Field, Course, Student, StudentList, FieldImage, CourseField
from Web_View.serializer import NewStudent


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
        messages.error(request, form.errors)
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
                # messages.info(request, f"You are now logged in as {username}.")
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
        try:
            student = Student.objects.get(user_id=request.user.id)
            course_fields.filter(course_id=student.course.id)
        except Student.DoesNotExist as e:
            pass
        fields = []
        for i in course_fields:
            fields.append(i.field)
        return render(request, 'index.html', {"fields": fields, "length": len(fields)})

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
        fields = StudentList.objects.all()
        return render(request, 'mylist.html', {"fields": [], "length": 0})

    return redirect('/login')


def Logout(request):
    logout(request)
    return redirect('/login')


class MyListManager(APIView):
    permission_classes = [AllowAny]

    @staticmethod
    def post(request, *args, **kwargs):
        data = request.data
        return Response(True)

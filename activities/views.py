from django.shortcuts import render
from django.views.generic import View

def index(request):
    return render(request, 'index.html')


class Login(View):
    def get(self, request):
        form = LoginForm()
        error = False
        return render(request, 'login.html', {'form': form, 'error': error})

    def post(self, request):
        form = LoginForm(self.request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = auth.authenticate(username=username, password=password)
            if user is not None and user.is_active:
                auth.login(request, user)
                return HttpResponseRedirect('/dashboard')
            else:
                error = True
                message = 'Invalid password/username!'
                return render(request, 'login.html', {'form': form, 'error': error, 'message': message})
        else:
            error = True
            message = 'Please fill out all the required forms!'
            return render(request, 'login.html', {'form': form, 'error': error, 'message': message})


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/login/')


def forgot(request):
    return render(request, 'forgot_password.html')


class Signup(View):
    def get(self, request):
        form = SignupForm()
        return render(request, 'signup.html', {'form': form})

    def post(self, request):
        form = SignupForm(self.request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            first_name = form.cleaned_data['firstname']
            last_name = form.cleaned_data['lastname']
            email = form.cleaned_data['email']
            role = form.cleaned_data['role']
            password = form.cleaned_data['password']
            username_results = User.objects.filter(username=username)
            if len(username_results) == 0:
                query = User.objects.create_user(username=username, first_name=first_name, last_name=last_name,
                                                 email=email, role=role, password=password)
                query.is_staff = True
                query.save()
                user_instance = User.objects.get(username=username)
                system_instance = role.objects.get(id=role)
                query = UserProfile(user=user_instance, role=system_instance)
                query.save()
                user = auth.authenticate(username=username, password=password)
                if user is not None:
                    auth.login(request, user)
                    return HttpResponseRedirect('/dashboard/')
                else:
                    error = True
                    message = "Ooops! Something went wrong."
                    return render(request, 'signup.html', {'form': form, 'message': message, 'error': error})
            else:
                error = True
                message = "Username already exists!"
                return render(request, 'signup.html', {'form': form, 'message': message, 'error': error})

        else:
            error = True
            message = "Please fill out the forms correctly."
            return render(request, 'signup.html', {'form': form, 'message': message, 'error': error})


def dashboard(request):
    if request.user.is_authenticated():
        fullname = request.user.get_full_name()
        user_instance = request.user
        system = UserProfile.objects.get(user=user_instance)
        return render(request, 'dashboard.html', {'fullname': fullname, 'firstname': user_instance.first_name,
                                                  'lastname': user_instance.last_name,
                                                  'email': user_instance.email, 'role': system.role.name})
    else:
        return HttpResponseRedirect('/login/')


class AddStudent(View):
    def post(self, request):
        # Get data
        first_name = request.POST['first_name']
        middle_name = request.POST['middle_name']
        last_name = request.POST['last_name']
        section_id = request.POST['section_id']
        # Get instance
        section_instance = Section.objects.get(id=section_id)
        # Check redundancy
        redundant = Student.objects.filter(first_name__iexact=first_name, middle_name__iexact=middle_name,
                                           last_name__iexact=last_name, section=section_instance)
        if len(redundant) == 0:
            query = Student(first_name=first_name, middle_name=middle_name, last_name=last_name,
                            section=section_instance)
            query.save()
        else:
            data = dict()
            data['error'] = True
            return HttpResponse(json.dumps(data), content_type="application/json")


class RemoveStudent(View):
    def post(self, request):
        student_id = request.POST['student_id']
        query = Student.objects.get(id=student_id)
        query.delete()
        return HttpResponse()


class SaveStudent(View):
    def post(self, request):
        section_id = request.POST['section_id']
        student_id = request.POST['student_id']
        last_name = request.POST['last_name']
        first_name = request.POST['first_name']
        middle_name = request.POST['middle_name']
        # Check redundancy
        section_instance = Section.objects.get(id=section_id)
        redundant = Student.objects.filter(first_name__iexact=first_name, middle_name__iexact=middle_name,
                                           last_name__iexact=last_name, section=section_instance)
        if len(redundant) == 0:
            query = Student.objects.get(id=student_id)
            query.first_name = first_name
            query.middle_name = middle_name
            query.last_name = last_name
            query.save()
            data = dict()
            data['error'] = False
            return HttpResponse(json.dumps(data), content_type="application/json")
        else:
            data = dict()
            data['error'] = True
            return HttpResponse(json.dumps(data), content_type="application/json")

        return HttpResponse()

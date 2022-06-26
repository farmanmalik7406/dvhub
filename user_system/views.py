import uuid

import bootstrap5.forms
import django.contrib.auth.hashers
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, HttpResponse
from django.views.generic import TemplateView
from django.contrib.auth.hashers import make_password
from user_system.forms import TodoForm, RegistrationForm
from user_system.mailer import Mailer
from user_system.models import Todo, UserVerification


# Create your views here.


class Index(TemplateView):
    template_name = "index.html"
    authorizer = Mailer()
    model = User
    verify_model = UserVerification

    def get(self, request, action=None, *args, **kwargs):
        if request.path == "/sendotp/":
            self.send_otp(request)

        if action == 'register':
            data = {"email": '', "first_name": '',
                    "last_name": ''}
            return render(request, 'registration/otp_verification.html', {"formdata": data, "isError": "false"})
        if request.user.is_authenticated:
            return render(request, self.template_name)
        return redirect('/accounts/login')

    def send_otp(self, request):
        email = request.GET['email']
        is_user = self.verify_model.objects.filter(email=email)
        print(not is_user)
        if not is_user:
            self.authorizer.gen_otp()
            user_verify_obj = self.verify_model(email=email, token=uuid.uuid4(), otp=self.authorizer.get_otp())
            user_verify_obj.save()
            self.authorizer.set_reciever(email)
            self.authorizer.send_otp()
            self.authorizer.end()
        else:
            self.authorizer.gen_otp()
            user = self.verify_model.objects.get(email=email)
            user.otp = self.authorizer.get_otp()
            user.save()
            self.authorizer.set_reciever(email)
            self.authorizer.send_otp()
            self.authorizer.end()

    def verify_otp(self, request):
        email = request.POST['email']
        otp = request.POST['otp']
        user = self.verify_model.objects.get(email=email)
        print(user.otp)
        if user.otp == otp:
            user.isVerified = True
            user.save()
            return True
        return False

    def post(self, request):
        if request.path == "/verifyotp/":
            data = {"email": request.POST['email'], "first_name": request.POST['first_name'],
                    "last_name": request.POST['last_name']}
            if self.verify_otp(request):
                form = RegistrationForm(data)
                return render(request, 'registration/register.html', {"form": bootstrap5.forms.render_form(form)})
            return render(request, 'registration/otp_verification.html',
                          {"formdata": data, "error": "otp not matched", "isError": "true"})
        if request.path == "/register_user/":

            return self.register(request)

    def register(self, request):
        email = request.POST['email']
        user = self.verify_model.objects.get(email=email)
        if user is not None:
            if user.isVerified:
                data = {k: v[0] for k, v in request.POST.lists()}
                data['password'] = make_password(data['password'])
                del data['csrfmiddlewaretoken']
                is_user = self.model.objects.filter(email=email)
                if is_user is None:
                    form = RegistrationForm(data)
                    if form.is_valid():
                        form.save()
                        return render(request,'registration/registration_success.html')
                return HttpResponse(f"User with email address {email} already exist please login <a href="">click here to login</a>")
            return redirect("/")


def get_todo(id):
    obj = Todo.objects.get(id=id)
    form = TodoForm(instance=obj)
    form.fields['create_date'].widget.attrs = {'class': 'datepicker'}
    form.fields['on_date'].widget.attrs = {'class': 'datepicker'}
    return HttpResponse(bootstrap5.forms.render_form(form))


def get_todos():
    obj = Todo.objects.all()
    return obj


def delete_todo(pk):
    obj = Todo.objects.filter(id=pk).delete()
    return redirect('/')


def update_todo(request):
    data = {k: v[0] for k, v in request.POST.lists()}
    id = data['pk_todo']
    del data['pk_todo']
    del data['csrfmiddlewaretoken']
    obj = Todo.objects.filter(id=id).update(**data)
    return redirect('/')


class Todos(TemplateView):
    model = Todo
    template_name = 'todos.html'

    def get(self, request, form=None, pk=None, action=None, *args, **kwargs):
        if request.user.is_authenticated:
            actions = {
                'delete': delete_todo,
                'get': get_todo
            }
            if pk is None:
                if form is None:
                    form = TodoForm()
                data = get_todos()
                return render(request, self.template_name, {"form": bootstrap5.forms.render_form(form), "data": data})
            return actions[action](pk)
        return redirect('/login')

    def get_context_data(self, **kwargs):
        return {"form": TodoForm()}

    def post(self, request):
        if 'pk_todo' not in request.POST:
            data = TodoForm(request.POST)
            print(data)
            if data.is_valid():
                data.save()
                return redirect("/todos")
            return self.get(request, form=data)
        return update_todo(request)

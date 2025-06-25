from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.views.generic import TemplateView
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages

from accounts.forms import MyUserCreationForm


class UserSignUpView(TemplateView):

    template_name = 'accounts/signup.html'

    def get(self, request, *args, **kwargs):
        form = MyUserCreationForm()
        context = {
            'form': form,
            "title":"Signup"
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('accounts:login')
        context = {
            'form': form,
        }
        return render(request, self.template_name, context)


class LogInView(TemplateView):

    template_name = 'accounts/login.html'

    def get(self, request, *args, **kwargs):
        form = AuthenticationForm()
        context = {
            'form': form,
            "title":"Login Page"
        }
        return render(request, self.template_name, context)

    from django.contrib import messages

    def post(self, request, *args, **kwargs):
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                if user.is_trainer:
                    return redirect('app:trainer_interns')
                elif user.is_intern:
                    return redirect('app:intern_dashboard')
                else:
                    messages.error(request, "У пользователя нет назначенной роли.")
            else:
                messages.error(request, "Неверное имя пользователя или пароль.")
        else:
            messages.error(request, "Неверное имя пользователя или пароль.")

        context = {
        'form': form,
        "title": "Вход"
        }
        return render(request, self.template_name, context)



class LogOutView(TemplateView):

    def get(self, request):
        logout(request)
        return redirect('accounts:login')

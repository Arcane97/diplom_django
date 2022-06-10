from django.contrib.auth import logout, login
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView

from works.forms import WorkForm, RegisterUserForm, LoginUserForm
from works.models import Work


class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'register.html'
    success_url = reverse_lazy('works:login')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('works:home')


class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'login.html'

    def get_success_url(self):
        return reverse_lazy('works:works_page')


def logout_user(request):
    logout(request)
    return redirect('works:login')


def works_page(request):
    if request.user.is_authenticated:
        works = Work.objects.filter(owner=request.user)
    else:
        return redirect('works:login')
    param = {'works': works}
    return render(request, 'works.html', param)


def work_page(request, work_id):
    work = Work.objects.get(pk=work_id)
    param = {'work': work}
    return render(request, 'work.html', param)


def new_work_page(request):
    if request.method == 'POST':
        form = WorkForm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.owner = request.user
            instance.save()
            return redirect(instance.get_absolute_url())

    else:
        form = WorkForm()

    param = {'form': form}
    return render(request, 'new_work.html', param)

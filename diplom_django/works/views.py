from django.contrib.auth import logout, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import LoginView
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView

from works.forms import WorkForm, RegisterUserForm, LoginUserForm, WorkFormCreate
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


class WorkUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    form_class = WorkForm
    model = Work
    template_name = 'work.html'

    def test_func(self):
        obj = self.get_object()
        return obj.owner == self.request.user


class StaffWorkUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    form_class = WorkFormCreate
    model = Work
    template_name = 'work.html'
    # success_url = reverse_lazy('works:staff_work_page')

    def test_func(self):
        obj = self.get_object()
        return obj.scientific_director == self.request.user

    def get_success_url(self):
        obj = self.get_object()
        return reverse('works:staff_work_page', args=[obj.pk])


def index(request):
    return render(request, 'index.html')


def logout_user(request):
    logout(request)
    return redirect('works:login')


def works_page(request):
    if request.user.is_authenticated:
        if request.user.is_staff:
            works = Work.objects.filter(scientific_director=request.user)
        else:
            works = Work.objects.filter(owner=request.user)
    else:
        return redirect('works:login')
    param = {'works': works}
    return render(request, 'works.html', param)


@login_required
def new_work_page(request):
    if not request.user.is_staff:
        return HttpResponseForbidden()
    if request.method == 'POST':
        form = WorkFormCreate(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.scientific_director = request.user
            instance.save()
            return redirect(instance.get_absolute_url())

    else:
        form = WorkFormCreate()

    param = {'form': form}
    return render(request, 'new_work.html', param)

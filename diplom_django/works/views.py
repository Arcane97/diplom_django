from django.contrib.auth import logout, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import LoginView
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView, ListView, DeleteView

from works.forms import WorkForm, RegisterUserForm, LoginUserForm, WorkFormCreate, WorksFilterForm
from works.models import Work, WorkType, AcademicYear


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


class WorkListView(LoginRequiredMixin, ListView):
    model = Work
    template_name = 'works.html'
    context_object_name = 'works'

    def _get_queryset_if_is_staff(self, **kwargs):
        if self.request.user.is_staff:
            return super().get_queryset().filter(scientific_director=self.request.user, **kwargs)
        else:
            return super().get_queryset().filter(owner=self.request.user, **kwargs)

    def get_queryset(self):
        work_type_slug = self.kwargs.get('work_type_id')
        year_slug = self.kwargs.get('year_id')

        if work_type_slug is None and year_slug is None:
            return self._get_queryset_if_is_staff()
        else:
            return self._get_queryset_if_is_staff(work_type__url_slug=work_type_slug,
                                                  academic_year__url_slug=year_slug)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = WorksFilterForm(initial={'work_type': self.kwargs.get('work_type_id'),
                                                   'academic_year': self.kwargs.get('year_id')})
        if self.kwargs.get('work_type_id'):
            context['work_type'] = WorkType.objects.get(url_slug=self.kwargs.get('work_type_id'))
        else:
            context['work_type'] = WorkType.objects.all()[0]
        return context


class WorkUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    form_class = WorkForm
    model = Work
    template_name = 'work.html'

    def form_valid(self, form):
        instance = form.save(commit=False)
        if 'change' in self.request.POST:
            instance.status = 'На проверке'
        return super(WorkUpdateView, self).form_valid(form)

    def test_func(self):
        obj = self.get_object()
        return obj.owner == self.request.user


class StaffWorkUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    form_class = WorkFormCreate
    model = Work
    template_name = 'work.html'

    def test_func(self):
        obj = self.get_object()
        return obj.scientific_director == self.request.user

    def get_success_url(self):
        obj = self.get_object()
        return reverse('works:staff_work_page', args=[obj.pk])

    def form_valid(self, form):
        instance = form.save(commit=False)
        if 'revision' in self.request.POST:
            instance.status = 'На доработке'
        if 'delete' in self.request.POST:
            return redirect(reverse('works:delete_work_page', kwargs={'pk': instance.pk}))
        if 'change' in self.request.POST and instance.is_accepted:
            instance.status = 'Работа принята'
        return super(StaffWorkUpdateView, self).form_valid(form)


class WorkDeleteView(DeleteView):
    model = Work
    success_url = reverse_lazy('works:works_page')
    template_name = 'work_delete.html'


def index(request):
    return render(request, 'index.html')


def logout_user(request):
    logout(request)
    return redirect('works:login')


# def works_page(request):
#     if request.user.is_authenticated:
#         if request.user.is_staff:
#             works = Work.objects.filter(scientific_director=request.user)
#         else:
#             works = Work.objects.filter(owner=request.user)
#     else:
#         return redirect('works:login')
#     form = WorksFilterForm(request.GET)
#     param = {'works': works, 'form': form}
#     return render(request, 'works.html', param)


def works_navform(request):
    work_type_id = request.POST.get('work_type')
    year_id = request.POST.get('academic_year')
    return redirect(reverse('works:works_pages', kwargs={'work_type_id': work_type_id, 'year_id': year_id}))


@login_required
def new_work_page(request, work_type_id):
    if not request.user.is_staff:
        return HttpResponseForbidden()
    work_type = WorkType.objects.get(url_slug=work_type_id)
    if request.method == 'POST':
        form = WorkFormCreate(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.scientific_director = request.user
            instance.work_type = work_type
            instance.save()
            return redirect(reverse('works:staff_work_page', kwargs={'pk': instance.pk}))

    else:
        form = WorkFormCreate()

    param = {'form': form, 'work_type': work_type}
    return render(request, 'new_work.html', param)

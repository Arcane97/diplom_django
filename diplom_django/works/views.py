from django.shortcuts import render, redirect

from works.forms import WorkForm
from works.models import Work


def works_page(request):
    works = Work.objects.all()
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

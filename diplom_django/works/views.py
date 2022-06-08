from django.shortcuts import render

from works.models import Work


def works_page(request):
    works = Work.objects.all()
    param = {'works': works}
    return render(request, 'works.html', param)


def work_page(request, work_id):
    work = Work.objects.get(pk=work_id)
    param = {'work': work}
    return render(request, 'work.html', param)

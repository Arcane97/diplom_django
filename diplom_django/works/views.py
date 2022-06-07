from django.shortcuts import render

from works.models import Work


def works_page(request):
    works = Work.objects.all()
    param = {'works': works}
    a = works[0].upload_date
    print(a.strftime("%d.%m.%Y"))
    return render(request, 'works.html', param)

from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


class WorkType(models.Model):
    name = models.CharField(max_length=255, verbose_name='Тип работы')
    url_slug = models.IntegerField(verbose_name='URL slug', blank=True, null=True, unique=True)

    def __str__(self):
        return self.name


class AcademicYear(models.Model):
    name = models.CharField(max_length=255, verbose_name='Учебный год')
    url_slug = models.IntegerField(verbose_name='URL slug', unique=True)

    def __str__(self):
        return self.name


class Work(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название работы', blank=True)
    file = models.FileField(upload_to='works/', verbose_name='Файл', blank=True)
    upload_date = models.DateField(auto_now=True, verbose_name='Дата загрузки')
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.CASCADE, verbose_name='Учебный год', blank=True,
                                      null=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Владелец работы', related_name='owner')
    work_type = models.ForeignKey(WorkType, on_delete=models.CASCADE, verbose_name='Тип работы')
    is_accepted = models.BooleanField(default=False, verbose_name='Работа принята')
    scientific_director = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Научный руководитель',
                                            related_name='scientific_director', blank=True, null=True)

    def __str__(self):
        return f'id:{self.id} {self.name}'

    def get_absolute_url(self):
        return reverse('works:work_page', kwargs={"pk": self.id})

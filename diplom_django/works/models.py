from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


class WorkType(models.Model):
    name = models.CharField(max_length=255, verbose_name='Тип работы')

    def __str__(self):
        return self.name


class Work(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название работы')
    file = models.FileField(upload_to='works/', verbose_name='Файл')
    upload_date = models.DateField(auto_now=True, verbose_name='Дата загрузки')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Владелец работы')
    work_type = models.ForeignKey(WorkType, on_delete=models.CASCADE, verbose_name='Тип работы')

    def __str__(self):
        return f'id:{self.id} {self.name}'

    def get_absolute_url(self):
        # todo разобраться почему не работает
        return reverse('works:work_page', kwargs={"work_id": self.id})

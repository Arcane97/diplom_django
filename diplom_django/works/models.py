from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


class WorkType(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Work(models.Model):
    name = models.CharField(max_length=255)
    file = models.FileField(upload_to='works/')
    upload_date = models.DateField(auto_now=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    work_type = models.ForeignKey(WorkType, on_delete=models.CASCADE)

    def __str__(self):
        return f'id:{self.id} {self.name}'

    def get_absolute_url(self):
        # todo разобраться почему не работает
        return reverse('works:work_page', kwargs={"work_id": self.id})

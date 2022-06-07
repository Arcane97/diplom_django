from django.contrib import admin

from works.models import Work, WorkType

admin.site.register(WorkType)
admin.site.register(Work)

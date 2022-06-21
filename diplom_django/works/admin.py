from django.contrib import admin

from works.models import Work, WorkType, AcademicYear

admin.site.register(WorkType)
admin.site.register(Work)
admin.site.register(AcademicYear)

from django.urls import path

from works.views import *

app_name = "works"
urlpatterns = [
    path('works/', works_page, name='works_page'),
    path('works/<int:work_id>/', work_page, name='work_page'),
    path('works/new_work_page', new_work_page, name='new_work_page')
]

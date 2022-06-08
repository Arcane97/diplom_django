from django.urls import path

from works.views import *

app_name = "works"
urlpatterns = [
    path('works/', works_page),
    path('works/<int:work_id>/', work_page, name='work_page'),
]

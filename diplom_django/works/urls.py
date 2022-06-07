from django.urls import path

from works.views import works_page

urlpatterns = [
    path('', works_page),
]

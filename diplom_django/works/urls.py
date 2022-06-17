from django.urls import path

from works.views import *

app_name = "works"
urlpatterns = [
    path('', index, name='home'),
    path('login/', LoginUser.as_view(), name='login'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('logout/', logout_user, name='logout'),
    path('works/', works_page, name='works_page'),
    path('works/<int:pk>/update', WorkUpdateView.as_view(), name='work_page'),
    path('works/<int:pk>/change', StaffWorkUpdateView.as_view(), name='staff_work_page'),
    path('works/new_work_page', new_work_page, name='new_work_page')
]

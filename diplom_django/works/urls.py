from django.urls import path

from works.views import *

app_name = "works"
urlpatterns = [
    path('', index, name='home'),
    path('login/', LoginUser.as_view(), name='login'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('logout/', logout_user, name='logout'),
    path('works/list/', WorkListView.as_view(), name='works_page'),
    path('works/list/<int:work_type_id>/<int:year_id>/', WorkListView.as_view(), name='works_pages'),
    path('works/<int:pk>/update', WorkUpdateView.as_view(), name='work_page'),
    path('works/<int:pk>/change', StaffWorkUpdateView.as_view(), name='staff_work_page'),
    path('works/new_work_page/<int:work_type_id>', new_work_page, name='new_work_page'),
    path('works/works_page_navform/', works_navform, name='works_page_navform'),
]

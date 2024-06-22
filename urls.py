"""
URL configuration for eazy_attendance project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from .views import *


urlpatterns = [
    path('admin/', admin.site.urls),
    path('',home),       
    path('login', login_view, name='login'),   
    path('logout', logout_view, name='logout'),  
    path('check-in/', check_in, name='check_in'),
    path('check-out/', check_out, name='check_out'),
    path('profile/', profile_setting, name='profile-setting'),
    path('company_profile/',company_profile,name='company_profile'),
    path('setting/holidays/', settings_view, name='settings'),
    path('employees/', employee_details_view, name='employees'),
    path('employee/<int:employee_id>/', employee_details_view, name='employee_details'),
    path('setting/shifts/', attendance_view, name='attendance'),
    path('edit/<int:shift_id>/', edit_shift, name='edit_shift'),
    path('attendance/', attendance_view, name='attendance_view'),
    path('holidays/', settings_view, name='settings_view'),
    path('delete_shift/<int:shift_id>/', delete_shift, name='delete_shift'),
    path('delete_holiday/<int:holiday_id>/', delete_holiday, name='delete_holiday'),   
    path('holiday_list/', holiday_list, name='holiday_list'),
    path('My_attendance/<int:employee_id>/', calendar_view, name='calendar'),    
    path('submit_attendance_request/', submit_attendance_request, name='submit_attendance_request'),
    path('submit_leave_request/', submit_leave_request, name='submit_leave_request'),
    path('add_holiday/', add_holiday, name='add_holiday'),
    path('add_shift/', add_shift, name='add_shift'),
    path('My_leaves/<int:employee_id>/', leaves_view, name='leaves'),
    path('leaves_request/<str:request_type>/', approve_request, name='approve_request'),
    path('attednance_request/<str:request_type>/', approve_request22, name='approve_request22'),
    path('company_holidays/', company_holidays, name='company_holidays'),
    path('apply_attendance_rules/', apply_attendance_rules, name='apply_attendance_rules'),
    path('support/',support,name='support'),
    path('contact/',contact,name='contact'),
    path('reports/',all_employees,name='all_employees'),
    path('fetch-employee-data/', fetch_employee_data, name='fetch_employee_data'),
    path("assignshift/",shift_assign_schedule,name="assign_shift"),
    path("approve_leave_request/",approve_leave_request,name="approve_leave_request"),
    path("reject_leave_request/",reject_leave_request,name="reject_leave_request"),
    path('approve_attendance_request/', approve_attendance_request, name='approve_attendance_request'),
    path('reject_attendance_request/', reject_attendance_request, name='reject_attendance_request'),
    path('generate_excel/<int:emp_id>/', generate_excel, name='generate_excel'),
    path('forgot-password/', forgot_password, name='forgot_password'),
    path('attendance_setting/', leave_setting, name='leave_setting'),
    path('penality_setting/', penalities_setting, name='penalities_setting'),

]
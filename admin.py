from django.contrib import admin

# Register your models here.

from .models import *
from eazy_attend import models

class AttendanceFilter(admin.ModelAdmin):
    list_display = ['employee','date','clock_in','clock_out','is_absent','is_week_off','is_late','is_early','is_present','is_leave','admin_photos']
    list_filter = ['employee','date','clock_in','clock_out','is_absent','is_week_off']





admin.site.register(Company)
admin.site.register(Employee)
admin.site.register(models.Attendance,AttendanceFilter)
# admin.site.register(Leave)
admin.site.register(AttendanceRequest)
admin.site.register(Shift)
admin.site.register(Holiday)
admin.site.register(LeaveRequest)
admin.site.register(CompanyPolicy)
admin.site.register(Approval)
admin.site.register(CompanyRules)
admin.site.register(CompanyPenality)









              




from django import forms
from .models import Attendance, Employee , Company , Shift ,  AttendanceRequest , LeaveRequest , Holiday

class ClockInImageForm(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = ['clock_in_image']



class ClockOutImageForm(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = ['clock_out_image']

class ProfileSettingsForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = [ 'phone_number', 'date_of_birth', 'city', 'state', 'zip_code', 'country']


class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['phone_number', 'date_of_birth', 'city', 'state', 'zip_code', 'country', 'department', 'position', 'report_to']


class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ['name', 'est_year', 'about', 'location', 'logo']  
        widgets = {
            'about': forms.Textarea(attrs={'rows': 5}),
        }


class ShiftForm(forms.ModelForm):
    class Meta:
        model = Shift
        fields = ['title', 'start_time', 'end_time', 'full_day_hours', 'half_day_hours', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']



class AttendanceRequestForm(forms.ModelForm):
    class Meta:
        model = AttendanceRequest
        fields = ['request_type', 'description']

    def __init__(self, *args, **kwargs):
        super(AttendanceRequestForm, self).__init__(*args, **kwargs)
        self.fields['request_type'].widget.attrs['readonly'] = True



class LeaveRequestForm(forms.ModelForm):
    class Meta:
        model = LeaveRequest
        fields = ['request_type', 'description', 'from_date', 'to_date']
        



class HolidayForm(forms.ModelForm):
    class Meta:
        model = Holiday
        fields = ['name', 'date', 'holiday_type']

class addshiftForm(forms.ModelForm):
    class Meta:
        model = Shift
        fields = ['title', 'start_time', 'end_time', 'full_day_hours', 'half_day_hours', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']


















    
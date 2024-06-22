
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone  
from django.db.models import Q
import datetime




class Company(models.Model):
    name = models.CharField(max_length=100)
    est_year = models.PositiveIntegerField()
    about = models.TextField()
    logo = models.ImageField(upload_to='company_logos/')
    location = models.CharField(max_length=100)

    def __str__(self):
        return self.name




class Shift(models.Model):
    monday=models.BooleanField(default=False)
    tuesday=models.BooleanField(default=False)
    wednesday=models.BooleanField(default=False)
    thursday=models.BooleanField(default=False)
    friday=models.BooleanField(default=False)
    saturday=models.BooleanField(default=False)
    sunday=models.BooleanField(default=False)
    title = models.CharField(max_length=100)
    start_time = models.TimeField()
    end_time = models.TimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    full_day_hours = models.IntegerField()
    half_day_hours = models.IntegerField()
    start_time_buffer = models.TimeField()
    end_time_buffer = models.TimeField()
    CompanyPenality = models.ForeignKey('CompanyPenality', on_delete=models.SET_NULL, null=True, blank=True)

   
    def __str__(self):
        return self.title



class Employee(models.Model):
    phone_number = models.BigIntegerField(default=0)  
    date_of_birth = models.DateField(null=True, blank=True)  
    city = models.CharField(max_length=100, default='Unknown')
    state = models.CharField(max_length=100, default='unknown')
    zip_code = models.BigIntegerField(default=421004) 
    country = models.CharField(max_length=100, default='unknown')
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='employee_images', null=True, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    employee_id = models.CharField(max_length=20, unique=True)
    department = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    report_to = models.ForeignKey('self', on_delete=models.SET_NULL, related_name='reports', null=True, blank=True)
    shift=models.ForeignKey(Shift, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"


from django.utils.safestring import mark_safe

class Attendance(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    date = models.DateField(null=True, blank=True)
    clock_in = models.TimeField(null=True, blank=True)
    clock_out = models.TimeField(null=True, blank=True)
    clock_in_image = models.ImageField(upload_to='clock_in_images/', null=True, blank=True)
    clock_out_image = models.ImageField(upload_to='clock_out_images/', null=True, blank=True)
    is_half_day=models.BooleanField(default=False)
    is_late=models.BooleanField(default=False)
    is_early=models.BooleanField(default=False)
    is_paid=models.BooleanField(default=True)
    is_absent=models.BooleanField(default=False)
    is_week_off=models.BooleanField(default=False)
    is_present=models.BooleanField(default=False)
    is_leave=models.BooleanField(default=False)
    coords = models.JSONField(null=True, blank=True,default=dict)   


    def admin_photos(self):
        if self.clock_in_image and self.clock_out_image:
            return mark_safe(f'<img src="{self.clock_in_image.url}" width="100" /> <img src="{self.clock_out_image.url}" width="100" />')
        elif self.clock_in_image:
            return mark_safe(f'<img src="{self.clock_in_image.url}" width="100" />')
        return None
    admin_photos.short_description = 'clock_in_and_out_Images'
    admin_photos.allow_tags = True

   



     


    def __str__(self):
        return f"{self.employee.user.username} - {self.date}"

    def clock_in_employee(self, *args, **kwargs):
        self.clock_in = timezone.now()
        self.save()

    def clock_out_employee(self, *args, **kwargs):
        self.clock_out = timezone.now()
        self.save()

    

    def save(self,*args,**kwargs):
        # Check if the clock in time is after the shift start time + buffer
        
        if self.clock_in:
            self.is_present = True
            if self.employee and self.employee.shift and self.employee.shift.start_time_buffer :
                if self.clock_in > self.employee.shift.start_time_buffer:
                # Mark as late
                    self.is_late = True
            print( self.clock_in > self.employee.shift.start_time_buffer, self.clock_in, self.employee.shift.start_time_buffer)


        if self.clock_out:
            if self.employee and self.employee.shift and self.employee.shift.end_time_buffer:
                if self.clock_out < self.employee.shift.end_time_buffer:
            # Mark as early
                    self.is_early = True

                
        # Get the current month and year
        current_month = datetime.date.today().month
        current_year = datetime.date.today().year
    

        # Filter attendance records for the current month
        current_month_attendance = Attendance.objects.filter(
            Q(is_late=True, employee=self.employee, date__month=current_month, date__year=current_year) |
            Q(is_early=True, employee=self.employee, date__month=current_month, date__year=current_year)
        )

        # Check if the count of late or early attendance exceeds the late deduction threshold
        if self.clock_in and self.clock_out and  current_month_attendance.count() > CompanyRules.objects.get(company=self.employee.company).late_deduction_after_days:
            

            if self.clock_in > self.employee.shift.start_time_buffer or self.clock_out < self.employee.shift.end_time_buffer:
                self.is_half_day = True

        super().save(*args, **kwargs)


# class Leave(models.Model):
#     STATUS_CHOICES = (
#         ('Pending', 'Pending'),
#         ('Approved', 'Approved'),
#         ('Disapproved', 'Disapproved'),
#     )

#     REQUEST_CHOICES = (
#         ('Sick Leave', 'Sick Leave'),
#         ('Maternity', 'Maternity'),
#         ('Paternity', 'Paternity'),    
#     ) 
    
    
#     employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
#     start_date = models.DateField()
#     end_date = models.DateField()
#     number_of_leaves = models.IntegerField(default=1)
#     reason = models.TextField()
#     status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
#     approver = models.ForeignKey('Employee', on_delete=models.CASCADE, related_name='approver', null=True, blank=True)
    

#     def __str__(self):
#         return f"{self.employee.user.username} from {self.start_date} to {self.end_date} - {self.status}"
    
class AttendanceRequest(models.Model): 
    REQUEST_CHOICES = (
        ('Check-in', 'Check-in'),              
        ('Check-out', 'Check-out'),
    )

    STATUS_CHOICES = (
        ('Pending', 'Pending'),             
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    )

    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    request_type = models.CharField(max_length=20, choices=REQUEST_CHOICES, default='Check-in')
    time = models.TimeField(null=True, blank=True)
    request_time = models.DateTimeField(auto_now_add=True)
    description = models.TextField(max_length=100)                  
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    reason = models.TextField(null=True, blank=True)
    date = models.DateField(null=True, blank=True)


    def __str__(self):
        return f"{self.employee.user.username} - {self.request_type.upper()} - {self.request_time} - {self.status}"



import uuid
class PasswordResetRequest(models.Model):
    key = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email

    
class Holiday(models.Model):
    name = models.CharField(max_length=100)
    date = models.DateField()
    holiday_type = models.CharField(max_length=50)

    def __str__(self):
        return self.name
    

class LeaveRequest(models.Model):


    REQUEST_CHOICES = (
        ('Sick Leave', 'Sick Leave'),              
        ('Maternity', 'Maternity'),
        ('Paternity', 'Paternity'),
        ('Compensatory Off', 'Compensatory Off'),
        ('Casual Leave', 'Casual Leave'),
        ('Holiday Leave', 'Holiday Leave'),
        ('paid Leave', 'paid Leave'),
        ('Unpaid Leave', 'Unpaid Leave'),
    )


    STATUS_CHOICES = (
        ('Pending', 'Pending'),             
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    )


    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    request_type = models.CharField(max_length=20, choices=REQUEST_CHOICES)
    number_of_leaves = models.IntegerField(default=1)
    request_time = models.DateTimeField(auto_now_add=True)
    description = models.TextField(max_length=100)                  
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    from_date = models.DateField(null=True, blank=True)
    to_date = models.DateField(null=True, blank=True)
    reason = models.TextField(null=True, blank=True)


    def __str__(self):
        return f"{self.request_type} - {self.employee}"
    

class CompanyPolicy(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    sick_leaves = models.PositiveIntegerField(default=0)
    paid_leaves = models.PositiveIntegerField(default=0)
    total_leaves = models.PositiveIntegerField(default=0)
    half_day_hours = models.PositiveIntegerField(default=4) 
    late_salary_deduction = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.company.name} - Leave and Attendance Policy"



class Approval(models.Model):
    APPROVAL_CHOICES = (
        ('Approved', 'Approved'),
        ('Denied', 'Denied'),
    )

    employee = models.ForeignKey(User, on_delete=models.CASCADE)
    request_type = models.CharField(max_length=20)  
    request_id = models.PositiveIntegerField()  
    approval_status = models.CharField(max_length=20, choices=APPROVAL_CHOICES)

    def __str__(self):
        return f"{self.employee.username} - {self.request_type} - {self.get_approval_status_display()}"
    



class CompanyRules(models.Model):
    company = models.OneToOneField('Company', on_delete=models.CASCADE)
    early_late_mark_deduction = models.DecimalField(max_digits=10, decimal_places=2, default=0.5, help_text="Deduction for every 3 early or late marks")
    consecutive_late_deduction_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0, help_text="Amount to be deducted for 3 consecutive late marks")
    monthly_late_deduction_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0, help_text="Amount to be deducted for 3 late marks in a month")
    weekly_late_deduction_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0, help_text="Amount to be deducted for 3 late marks in a week")
    late_deduction_after_days = models.PositiveIntegerField(default=7, help_text="Number of days after which late deduction will apply")
    early_deduction_after_days = models.PositiveIntegerField(default=7, help_text="Number of days after which early deduction will apply")
    monthly_leave = models.DecimalField(max_digits=10, decimal_places=2, default=0, help_text="Amount to be deducted for 1 month of leave")


    
    def __str__(self):
        return f"Rules for {self.company}"
    



class Logging(models.Model):
    created_at=models.DateTimeField(("Date"),auto_now=False, auto_now_add=True)
    log=models.CharField(max_length=500)


class CompanyPenality(models.Model):
    RULE_CHOICES = [
        ('All', 'All'),
        ('Every', 'Every'),
        ('Consecutive', 'Consecutive'),
    ]
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    rules = models.CharField(max_length=100, choices=RULE_CHOICES)
    period=models.PositiveIntegerField()
    penalty=models.FloatField()
    start_date = models.DateField()
    end_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.rules}"




























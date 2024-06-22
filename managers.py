from django.db import models
from .models import *
import datetime
import threading





class CreateAttendanceThreading(threading.Thread):
    def __init__(self, employee):
        """
        Initializes the CreateAttendanceThreading class.

        Args:
            employee (Employee): The employee object.
        """
        self.employee = employee
        # Call the init method of the parent class (Thread)
        threading.Thread.__init__(self)
    def run(self):
        """
        Run method that is called when the thread is started.
        It creates a new attendance record for the employee, and if the clock in
        and clock out times for the previous day are not set, marks the
        employee as absent.
        """
        try:
            from eazy_attend.models import Attendance
            # Create a new attendance record for the employee
            # Attendance.objects.create(employee=self.employee)


             # Calculate the date for the previous day
            previous_day = datetime.date.today() - datetime.timedelta(days=1)
            print(previous_day)

            # Get the attendance record for the previous day
            emp_aten = Attendance.objects.get_or_create(
                employee=self.employee,
                date=previous_day
            )[0]
            print(emp_aten)

            weekday_names = {
                0: self.employee.shift.monday,
                1: self.employee.shift.tuesday,
                2: self.employee.shift.wednesday,
                3: self.employee.shift.thursday,
                4: self.employee.shift.friday,
                5: self.employee.shift.saturday,
                6: self.employee.shift.sunday
            }
            print(weekday_names[previous_day.weekday()])
            # If the clock in and clock out times for the previous day are not set,
            # mark the employee as absent
            if not emp_aten.clock_in and not emp_aten.clock_out:
                emp_aten.is_absent = weekday_names[previous_day.weekday()]
                emp_aten.is_week_off= not weekday_names[previous_day.weekday()]
                emp_aten.save()
            
             # Determine if the previous day was a week off
                # is_week_off = weekday_names[previous_day.weekday()]
                # If the clock in and clock out times for the previous day are not set,
                # mark the employee as absent or on a week off
                # if is_week_off:
                #     emp_aten.is_week_off = True
                # else:
                #     emp_aten.is_absent = True
                    
                # emp_aten.save()

            
            # if not emp_aten.clock_in and not emp_aten.clock_out:

        except Exception as e:
            # Print any exception that occurs
            print(e)



def create_current_day_attendances():
    """
    Function to create attendance records for all employees.

    This function uses multiple threads to create attendance records
    concurrently, which improves performance.
    """
    # Iterate over all employees
    for employee in Employee.objects.all():
        # Create a new thread for each employee and start it
        thread = CreateAttendanceThreading(employee)
        thread.start()



# class CreateAttendanceThreading(threading.Thread):
#     def __init__(self, employee):
#         """
#         Initializes the CreateAttendanceThreading class.

#         Args:
#             employee (Employee): The employee object.
#         """
#         self.employee = employee
#         threading.Thread.__init__(self)

#     def run(self):
#         """
#         Run method that is called when the thread is started.
#         It creates a new attendance record for the employee, and if the clock in
#         and clock out times for the previous day are not set, marks the
#         employee as absent.
#         """
#         try:
#             # Calculate the date for the previous day
#             previous_day = datetime.date.today() - datetime.timedelta(days=1)
#             print(previous_day)

#             # Get the attendance record for the previous day
#             emp_aten = Attendance.objects.get_or_create(
#                 employee=self.employee,
#                 date=previous_day
#             )[0]
#             print(emp_aten)

#             # Define weekday names and corresponding shifts
#             weekday_names = {
#                 0: self.employee.shift.monday,
#                 1: self.employee.shift.tuesday,
#                 2: self.employee.shift.wednesday,
#                 3: self.employee.shift.thursday,
#                 4: self.employee.shift.friday,
#                 5: self.employee.shift.saturday,
#                 6: self.employee.shift.sunday
#             }
#             print(weekday_names[previous_day.weekday()])

#             # If the clock in and clock out times for the previous day are not set,
#             # mark the employee as absent
#             if not emp_aten.clock_in and not emp_aten.clock_out:
#                 emp_aten.is_absent = weekday_names[previous_day.weekday()]
#                 emp_aten.is_week_off = not weekday_names[previous_day.weekday()]
#                 emp_aten.save()

#             # Apply penalties if the employee was absent, half-day, or late
#             if emp_aten.is_absent or emp_aten.is_half_day or emp_aten.is_late:
#                 self.apply_penalties()

#         except Exception as e:
#             # Print any exception that occurs
#             print(e)

#     def apply_penalties(self):
#         """
#         Apply penalties based on the company's penalty rules.
#         """
#         try:
#             # Get the company of the employee
#             company = self.employee.company

#             # Get the penalty rules for the company specific to the employee's shift
#             penalty = CompanyPenality.objects.get(company=company, shift=self.employee.shift)
#             if not penalty:
#                 return
            
            
#             match penalty.period:
#                 case "all":
#                     pass
#                 case "every":
#                     pass
#                 case "consicutively":
#                     ... 
                    

#             # Apply the penalties
#             if penalty.rules and penalty.period and penalty.penalty:
#                     # Calculate the penalty period
#                     end_date = datetime.date.today()
#                     start_date = end_date - datetime.timedelta(days=int(penalty.period))

#                     # Get the attendance records within the penalty period
#                     attendance_records = Attendance.objects.filter(employee=self.employee, date__range=[start_date, end_date])

#                     # Apply penalty if attendance rules are violated
#                     #putting start date and end date in the query 
                    
                    
#                     lates = attendance_records.get (is_late=True,date__range=[start_date, end_date]).count()  
#                     early = attendance_records.get(is_early=True,date__range=[start_date, end_date]).count()
#                     total = lates + early
                    
                    
#                     if total >= int(penalty.rules):
#                         self.employee.is_penalty = True
#                         self.employee.save()                        
                
#         except Exception as e:
#             print(e)

    

# def create_current_day_attendances():
#     """
#     Function to create attendance records for all employees.

#     This function uses multiple threads to create attendance records
#     concurrently, which improves performance.
#     """
#     # Iterate over all employees
#     for employee in Employee.objects.all():
#         # Create a new thread for each employee and start it
#         thread = CreateAttendanceThreading(employee)
#         thread.start()










from django.urls import path, register_converter
import datetime
from . import views


class DateConverter:
    regex = r'\d{4}-\d{1,2}-\d{1,2}'
    format = '%Y-%m-%d'


    def to_python(self, value: str) -> datetime.date:
        return datetime.datetime.strptime(value, self.format).date()
    

    def to_url(self, value: datetime.datetime) -> str:
        return value.strftime(self.format)


register_converter(DateConverter, 'date')


urlpatterns = [
    path(
        'clinics/list', 
        view=views.get_clinics, 
        name='GET Clinics'),
    path(
        'clinics/add', 
        view=views.add_clinic, 
        name='POST Clinic'),
    path(
        'clinics/<int:clinic_id>/doctors/list', 
        view=views.get_clinic_doctors, 
        name="GET Clinic's Doctors"),
    path(
        'doctors/list', 
        view=views.get_doctors, 
        name='GET Doctors'),
    path(
        'doctors/<int:doctor_id>/schedules/list', 
        view=views.get_doctor_schedules, 
        name="GET Doctor's schedules"),
    path(
        'doctors/<int:doctor_id>/schedules/<date:schedule_date>/slots/list', 
        view=views.get_doctor_appointment_slots, 
        name="GET Doctor's appointment slots"),
    path(
        'patients/list', 
        view=views.get_patients, 
        name='GET Patients'),
]
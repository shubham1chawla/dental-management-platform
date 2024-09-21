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
        'clinics/<int:clinic_id>', 
        view=views.get_clinic, 
        name='GET Specific Clinic'),
    path(
        'clinics/add', 
        view=views.add_clinic, 
        name='POST Clinic'),
    path(
        'clinics/<int:clinic_id>/update', 
        view=views.update_clinic, 
        name='PUT Clinic'),
    path(
        'clinics/<int:clinic_id>/doctors/list', 
        view=views.get_clinic_doctors, 
        name="GET Clinic's Doctors"),
    path(
        'clinics/<int:clinic_id>/doctors/<int:doctor_id>/schedules/list', 
        view=views.get_clinic_doctor_schedules, 
        name="GET Clinic's Doctor's schedules"),
    path(
        'clinics/<int:clinic_id>/patients/list', 
        view=views.get_clinic_patients, 
        name="GET Clinic's Patients"),
    path(
        'doctors/list', 
        view=views.get_doctors, 
        name='GET Doctors'),
    path(
        'doctors/<int:doctor_id>', 
        view=views.get_doctor, 
        name='GET Specific Doctor'),
    path(
        'doctors/add', 
        view=views.add_doctor, 
        name='POST Doctor'),
    path(
        'doctors/<int:doctor_id>/update', 
        view=views.update_doctor, 
        name='PUT Doctor'),
    path(
        'doctors/<int:doctor_id>/specialties/list', 
        view=views.get_doctor_specialties, 
        name="GET Doctor's specialties"),
    path(
        'doctors/<int:doctor_id>/clinics/list', 
        view=views.get_doctor_clinics, 
        name="GET Doctor's Clinics"),
    path(
        'doctors/<int:doctor_id>/patients/list', 
        view=views.get_doctor_patients, 
        name="GET Doctor's Patients"),
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
    path(
        'patients/<int:patient_id>', 
        view=views.get_patient, 
        name='GET Specific Patient'),
    path(
        'patients/add', 
        view=views.add_patient, 
        name='POST Patient'),
    path(
        'patients/<int:patient_id>/appointments/list', 
        view=views.get_patient_appointments, 
        name="GET Patient's appointments"),
    path(
        'patients/<int:patient_id>/appointments/last', 
        view=views.get_patient_last_appointments, 
        name="GET Patient's last appointments"),
    path(
        'patients/<int:patient_id>/appointments/next', 
        view=views.get_patient_next_appointments, 
        name="GET Patient's next appointments"),
    path(
        'procedures/list', 
        view=views.get_procedures, 
        name='GET Procedures'),
    path(
        'appointments/<int:appointment_id>/procedures/list', 
        view=views.get_appointment_procedures, 
        name="GET Appointment's procedures"),
]

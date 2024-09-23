# Dental Management Platform

This `django` project is a patient and provider management platform. Key features includes - 
1. [Clinics Management](#clinics-management) 
    - [List all clinics (w/ number of affiliated doctors and patients)](#list-all-clinics)
    - [Add new clinics](#add-new-clinics)
    - [Edit clinic's details](#edit-clinics-details)
    - [View affiliated doctors](#view-affiliated-doctors)
    - [Add new doctor affiliation (w/ office address and working hours)](#add-new-doctor-affiliation)
    - [Edit existing doctor affiliations](#edit-existing-doctor-affiliations)
    - [Remove doctor affiliations](#remove-doctor-affiliations)
2. Doctors Management
    - List all doctors (w/ specialties and number of affiliated clinics and patients)
    - Add new doctors
    - Edit doctor's details
    - View affiliated clinics
    - View affiliated patients
3. Patients Management
    - List all patients (w/ last and next visit's date, doctor, and procedure)
    - Add new patients
    - Edit patient's details
    - List all visits (w/ doctor's notes, if present)
    - Add new visits
    - View upcoming visit (w/ when the visit's booking date)

> [!NOTE]
> The project made the following assumptions - 
> 1. Doctor's appointment slots are 1 hour long with 5 minutes buffer at the end.
> 2. Doctor can only work 1 shift on a specific weekday. For instance, if a doctor works at Clinic 1 on Monday, users can not add this doctor's schedule to another clinic for Monday. Users must remove the affiliation with Clinic 1 first before adding Clinic 2's affiliation for Monday.

## Local Setup

- You will need Python version `3.12.6` to run this project. Please refer to the [Python's documentation](https://www.python.org/downloads/) to install it on your system.
- Make sure you have `poetry` installed on your system. If not, use `pip install poetry` or `pip3 install poetry` command.
- Configure `poetry` to create virtual environments inside project directory by executing `poetry config virtualenvs.in-project true` command.
- Install dependencies by executing `poetry install` command.
- To enter the virtual environment, use `poetry shell` command.
- Create a super user for development using `python manage.py createsuperuser` command. Make sure you remember the credentials.
- Migrate local `sqlite3` database with necessary tables using `python manage.py migrate` command.
- Execute `python manage.py runserver` command to run the server.
- Navigate to [localhost:8000](http://localhost:8000/) to access the application.
- Use the super user's credentials to login to the application.

## Features

### Clinics Management

#### List all clinics

![All clinics screenshot](/screenshots/all-clinics.png)

API Endpoint - 
```
GET /api/clinics/list
```

API Response (200) -
```
[
  {
    "id": 1,
    "address": {
      "id": 1,
      "street_address_1": "100 N Dental Rd",
      "street_address_2": null,
      "city": "Tempe",
      "state": "Arizona",
      "zipcode": "85281"
    },
    "name": "Tempe Dental Clinic",
    "email": "tempe.dental@clinic.com",
    "phone_number": "+19452161541"
  },
  {
    "id": 2,
    "address": {
      "id": 4,
      "street_address_1": "52st Clinic St",
      "street_address_2": null,
      "city": "Mesa",
      "state": "Arizona",
      "zipcode": "85202"
    },
    "name": "Mesa Dental Clinic",
    "email": "mesa.dental@clinic.com",
    "phone_number": "+14805121821"
  }
]
```

#### Add new clinics

![Add clinics screenshot](/screenshots/add-clinic.png)

API Endpoint -
```
POST /api/clinics/add
```

Request body - 
```
{
  "name": "Test Clinic",
  "email": "test@clinic.com",
  "phone_number": "+19452161548",
  "address": {
    "street_address_1": "1234 E Clinic St",
    "street_address_2": null,
    "city": "Mesa",
    "state": "Arizona",
    "zipcode": "85202"
  }
}
```

#### Edit clinic's details

![Edit clinic screenshot](/screenshots/edit-clinic.png)

API Endpoint -
```
PUT /api/clinics/<clinic_id>/update
```

Request body - 
```
{
  "name": "Test Clinic",
  "email": "test@clinic.com",
  "phone_number": "+19452161548",
  "address": {
    "street_address_1": "1234 E Clinic St",
    "street_address_2": null,
    "city": "Mesa",
    "state": "Arizona",
    "zipcode": "85202"
  }
}
```

#### View affiliated doctors

![View affiliated doctors screenshot](/screenshots/affiliated-doctors.png)

API Endpoint - 
```
GET /api/clinics/<clinic_id>/doctors/<doctor_id>/schedules/list
```

API Response (200) -
```
[
  {
    "id": 1,
    "clinic": { ... },
    "doctor": { ... },
    "office_address": {
      "id": 2,
      "street_address_1": "100 N Clinic Rd",
      "street_address_2": "Suite 101",
      "city": "Tempe",
      "state": "Arizona",
      "zipcode": "85281"
    },
    "weekday": 0,
    "start_time": "08:00:00",
    "end_time": "16:00:00",
    "clinic_id": 1,
    "doctor_id": 1
  }
]
```

#### Add new doctor affiliation

![Add new doctor affiliation screenshot](/screenshots/add-new-doctor-affiliation.gif)

API Endpoint -
```
POST /api/clinics/<clinic_id>/doctors/<doctor_id>/schedules/add
```

Request body - 
```
{
  "weekday": 4,
  "start_time": "10:00:00",
  "end_time": "12:00:00",
  "office_address": {
    "street_address_1": "1234 S Road Dr",
    "city": "NYC",
    "state": "New York",
    "zipcode": "12345-1234"
  }
}
```

#### Edit existing doctor affiliations

![Edit doctor affiliation screenshot](/screenshots/edit-doctor-affiliation.gif)

API Endpoint -
```
PUT /api/clinics/<clinic_id>/doctors/<doctor_id>/schedules/<schedule_id>/update
```

Request body - 
```
{
  "weekday": 4,
  "start_time": "10:00:00",
  "end_time": "15:00:00",
  "office_address": {
    "street_address_1": "1234 S Road Dr",
    "city": "NYC",
    "state": "New York",
    "zipcode": "12345-1234"
  }
}
```

#### Remove doctor affiliations

![Remove doctor affiliation screenshot](/screenshots/remove-doctor-affiliation.png)

API Endpoint -
```
DELETE /api/clinics/<clinic_id>/doctors/<doctor_id>/schedules/<schedule_id>/remove
```

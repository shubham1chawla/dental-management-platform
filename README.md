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
2. [Doctors Management](#doctors-management)
    - [List all doctors (w/ specialties and number of affiliated clinics and patients)](#list-all-doctors)
    - [Add new doctors](#add-new-doctors)
    - [Edit doctor's details](#edit-doctors-details)
    - [View affiliated clinics & patients](#view-affiliated-clinics--patients)
3. [Patients Management](#patients-management)
    - [List all patients (w/ last and next visit's date, doctor, and procedure)](#list-all-patients)
    - [Add new patients](#add-new-patients)
    - [Edit patient's details](#edit-patients-details)
    - [List all visits (w/ doctor's notes, if present)](#list-all-visits)
    - [Add new visits](#add-new-visits)


> [!NOTE]
> The project made the following assumptions - 
> 1. Doctor's appointment slots are 1 hour long with 5 minutes buffer at the end.
> 2. Doctor can only work 1 shift on a specific weekday. For instance, if a doctor works at Clinic 1 on Monday, users can not add this doctor's schedule to another clinic for Monday. Users must remove the affiliation with Clinic 1 first before adding Clinic 2's affiliation for Monday.

## Project Structure

```
[ROOT]
├── api                # <-- Contains all the REST API-related routes
├── components         # <-- Contains reusable UI components using django_components
├── core               # <-- Contains django's main settings.py and other configurations
├── service            # <-- Contains application's backend and interface to all the database-related methods
└── web                # <-- Contains all the webpages and user-facing routes
    └── templates      # <-- Contains all the HTML templates
```

## Local Setup

> [!IMPORTANT]
> The project uses the following tech-stack. If you don't have any of these installed on your system, please refer to the relevant documentation.
> 1. **Docker** - The project uses Postgres database using Docker. If you don't have Docker installed on your system, please refer to [Docker's installation documentation](https://docs.docker.com/engine/install/).
> 2. **Python 3.12.6** - You will need Python version `3.12.6` to run this project. Please refer to the [Python's documentation](https://www.python.org/downloads/) to install it on your system.
> 3. **pip** - You will need to install `pip` to resolve project's Python dependencies. Please refer to the [pip installation documentation](https://pip.pypa.io/en/stable/installation/) to install `pip` on your system.
> 4. **Poetry Dependency Manager** - Make sure you have `poetry` installed on your system. If not, use `pip install poetry` or `pip3 install poetry` command. Configure `poetry` to create virtual environments inside project directory by executing `poetry config virtualenvs.in-project true` command.

- **Step 1:** Start by running the `postgres` Docker container on your system. Use the following command to run the database.

```sh
docker run -d --name dentaldb -e POSTGRES_DB=postgres -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=postgres -e PGDATA=/var/lib/postgresql/data/pgdata -v ./db:/var/lib/postgresql/data -p "5432:5432" postgres
```

> [!NOTE]
> You might see an error that Docker was unable to expose port `5432` on your system. This error can be because of a local instance of `postgres` or `pgAdmin` that is running on your system.
> In this case, 
> - You can either shut the local `postgres` or `pgAdmin` server, or 
> - Change the port in **Step 1** and in the [settings.py](/core/settings.py) file.

> [!NOTE]
> For Windows - 
> 1. You will need to use a bash-based terminal. Assuming you have `git` installed on your system, you can use `Git Bash` for next steps.
> 2. For creating super user, you will need to append `winpty` to the command. Final command will be `winpty python manage.py createsuperuser` to create the super user in Step 5.

- **Step 2:** Install dependencies by executing `poetry install` command.
- **Step 3:** To enter the virtual environment, use `poetry shell` command.
- **Step 4:** Migrate local `postgres` database with necessary tables using `python manage.py migrate` command.
- **Step 5:** Create a super user for development using `python manage.py createsuperuser` command. **Make sure you remember the credentials.**
- **Step 6:** Execute `python manage.py runserver` command to run the server.
- **Step 7:** Navigate to [localhost:8000](http://localhost:8000/) to access the application.
- **Step 8:** Use the super user's credentials (Step 5) to login to the application.

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

### Doctors Management

#### List all doctors

![All doctors screenshot](/screenshots/all-doctors.png)

API Endpoint - 
```
GET /api/doctors/list
```

API Response (200) -
```
[
  {
    "id": 1,
    "npi": "1122334455",
    "name": "John Donson",
    "email": "john.donson@doctor.com",
    "phone_number": "+14807651234"
  },
  {
    "id": 2,
    "npi": "9871123761",
    "name": "Tony Stark",
    "email": "tony.stark@doctor.com",
    "phone_number": "+19452171821"
  }
]
```

#### Add new doctors

![Add new doctors screenshot](/screenshots/add-new-doctor.png)

API Endpoint -
```
POST /api/doctors/add
```

Request body - 
```
{
  "name": "Bruce Wayne",
  "email": "bruce.wayne@doctor.com",
  "phone_number": "+19452161776",
  "npi": 3412567812,
  "specialties": [1, 2]
}
```

#### Edit doctor's details

![Edit doctor screenshot](/screenshots/edit-doctor.png)

API Endpoint -
```
PUT /api/doctors/<doctor_id>/update
```

Request body - 
```
{
  "name": "Bruce Wayne",
  "email": "bruce.wayne@doctor.com",
  "phone_number": "+19452161776",
  "npi": 3412567812,
  "specialties": [1, 2]
}
```

#### View affiliated clinics & patients

![Doctor page screenshot](/screenshots/doctor-page.png)

### Patients Management

#### List all patients

![All patients screenshot](/screenshots/all-patients.png)

API Endpoint - 
```
GET /api/patients/list
```

API Response (200) -
```
[
  {
    "id": 1,
    "address": {
      "id": 3,
      "street_address_1": "1234 S House Rd",
      "street_address_2": "Apt 10",
      "city": "Mesa",
      "state": "Arizona",
      "zipcode": "85202"
    },
    "name": "Alice Bob",
    "email": "alice.bob@gmail.com",
    "phone_number": "+14809761234",
    "dob": "1995-09-01",
    "ssn": 9876,
    "gender": "F"
  },
  {
    "id": 2,
    "address": {
      "id": 7,
      "street_address_1": "#1 Bruce St",
      "street_address_2": null,
      "city": "Chicago",
      "state": "Illinois",
      "zipcode": "77212-9123"
    },
    "name": "Bruce Wayne",
    "email": "bruce@wayne.com",
    "phone_number": "+14802981234",
    "dob": "1981-09-05",
    "ssn": 6542,
    "gender": "M"
  }
]
```

#### Add new patients

![Add new patients screenshot](/screenshots/add-new-patient.png)

API Endpoint -
```
POST /api/patients/add
```

Request body - 
```
{
  "name": "Pepper Pots",
  "dob": "1998-03-28",
  "ssn": 7621,
  "email": "pepper.pots@stark.com",
  "phone_number": "+19452161991",
  "gender": "F",
  "address": {
    "street_address_1": "87 E Famous Rd",
    "street_address_2": "#151",
    "city": "Phoenix",
    "state": "Arizona",
    "zipcode": "87654-1234"
  }
}
```

#### Edit patient's details

![Edit patient screenshot](/screenshots/edit-patient.png)

API Endpoint -
```
PUT /api/patients/<patient_id>/update
```

Request body - 
```
{
  "name": "Pepper Pots",
  "dob": "1998-03-28",
  "ssn": 7621,
  "email": "pepper.pots@stark.com",
  "phone_number": "+19452161991",
  "gender": "F",
  "address": {
    "street_address_1": "87 E Famous Rd",
    "street_address_2": "#151",
    "city": "Phoenix",
    "state": "Arizona",
    "zipcode": "87654-1234"
  }
}
```

#### List all visits

![All visits screenshot](/screenshots/all-visits.png)

API Endpoint - 
```
GET /api/patients/1/appointments/list
```

API Response (200) -
```
[
  {
    "id": 1,
    "clinic": { ... },
    "doctor": { ... },
    "patient": { ... },
    "date": "2024-09-23",
    "start_time": "11:00:00",
    "end_time": "11:55:00",
    "notes": "Great dental health!",
    "created_at": "2024-09-22T23:13:12.468891Z",
    "modified_at": "2024-09-23T01:53:09.446593Z",
    "clinic_id": 1,
    "doctor_id": 1,
    "patient_id": 1
  }
]
```
#### Add new visits

![Add new visit screenshot](/screenshots/add-new-visit.png)

API Endpoint -
```
POST /api/patients/<patient_id>/appointments/add
```

Request body - 
```
{
  "procedure_id": 4,
  "clinic_id": 1,
  "doctor_id": 2,
  "date": "2024-09-23",
  "start_time": "13:00:00,
  "end_time": "13:55:00",
}
```
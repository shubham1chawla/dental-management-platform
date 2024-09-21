(function () {
    const form = document.querySelector('#patient-form');
    if (!form) return;

    const button = document.querySelector('#submit-button');

    const addErrorMessage = () => {
        const alert = document.createElement('div');
        alert.className = 'alert alert-danger mt-4';
        alert.role = 'alert';
        alert.innerHTML = 'An error occured while saving the patient. Please try again later';
        form.appendChild(alert);
        button.removeAttribute('disabled');
    }

    const addPatient = async (patient) => {
        const response = await fetch('/api/patients/add', {
            body: JSON.stringify(patient),
            method: 'POST',
            headers: new Headers({ 'content-type': 'application/json' }),
        });
        if (response.ok) {
            window.location.pathname = '/patients';
            return;
        }
        addErrorMessage();
    };

    const updatePatient = async (patientId, patient) => {
        const response = await fetch(`/api/patients/${patientId}/update`, {
            body: JSON.stringify(patient),
            method: 'PUT',
            headers: new Headers({ 'content-type': 'application/json' }),
        });
        if (response.ok) {
            window.location.pathname = `/patients/${patientId}`;
            return;
        }
        addErrorMessage();
    };

    form.addEventListener('submit', (e) => {
        e.preventDefault();
        button.setAttribute('disabled', true);

        const address = {
            street_address_1: null,
            street_address_2: null,
            city: null,
            state: null,
            zipcode: null,
        };

        for (const key of Object.keys(address)) {
            const { value } = document.querySelector(`#${key}-input`);
            if (key !== 'street_address_2' && ((!value || !value.length))) {
                document.querySelector(`${key}-error`).innerHTML = 'This is required field!';
                return;
            }
            address[key] = value || null;
        }

        const patient = {
            name: null,
            email: null,
            phone_number: null,
            dob: null,
            ssn: null,
            gender: null,
        };

        for (const key of Object.keys(patient)) {
            const { value } = document.querySelector(`#${key}-input`);
            if (!value || !value.length) {
                document.querySelector(`${key}-error`).innerHTML = 'This is required field!';
                return;
            }
            patient[key] = value;
        }

        patient.address = address;
        patient.ssn = parseInt(patient.ssn);
        const patientId = form.getAttribute('data-id') || null;

        if (patientId) {
            updatePatient(patientId, patient);
        } else {
            addPatient(patient);
        }
    });
})();
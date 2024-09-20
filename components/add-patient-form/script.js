(function () {
    const form = document.querySelector('#add-patient-form');
    if (!form) return;

    form.addEventListener('submit', (e) => {
        e.preventDefault();
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
        patient.phone_number = '+1' + patient.phone_number.replaceAll(' ', '');

        // Loading state
        const button = document.querySelector('#submit-button');
        button.setAttribute('disabled', true);

        fetch('/api/patients/add', {
            body: JSON.stringify(patient),
            method: 'POST',
            headers: new Headers({ 'content-type': 'application/json' }),
        }).then((response) => {
            if (response.status !== 200) {
                const alert = document.createElement('div');
                alert.className = 'alert alert-danger mt-4';
                alert.role = 'alert';
                alert.innerHTML = 'An error occured while saving the patient. Please try again later';
                form.appendChild(alert);
                button.removeAttribute('disabled');
                return;
            }
            window.location.pathname = '/patients';
        });
    });
})();
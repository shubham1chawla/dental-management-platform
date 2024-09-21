(function () {
    const form = document.querySelector('#client-form');
    if (!form) return;

    const button = document.querySelector('#submit-button');

    const addErrorMessage = () => {
        const alert = document.createElement('div');
        alert.className = 'alert alert-danger mt-4';
        alert.role = 'alert';
        alert.innerHTML = 'An error occured while saving the clinic. Please try again later';
        form.appendChild(alert);
        button.removeAttribute('disabled');
    }

    const addClinic = async (clinic) => {
        const response = await fetch('/api/clinics/add', {
            body: JSON.stringify(clinic),
            method: 'POST',
            headers: new Headers({ 'content-type': 'application/json' }),
        });
        if (response.ok) {
            window.location.pathname = '/clinics';
            return;
        }
        addErrorMessage();
    };

    const updateClinic = async (clinicId, clinic) => {
        const response = await fetch(`/api/clinics/${clinicId}/update`, {
            body: JSON.stringify(clinic),
            method: 'PUT',
            headers: new Headers({ 'content-type': 'application/json' }),
        });
        if (response.ok) {
            window.location.pathname = `/clinics/${clinicId}`;
            return;
        }
        addErrorMessage();
    }

    form.addEventListener('submit', async (e) => {
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

        const clinic = {
            name: null,
            email: null,
            phone_number: null,
        };

        for (const key of Object.keys(clinic)) {
            const { value } = document.querySelector(`#${key}-input`);
            if (!value || !value.length) {
                document.querySelector(`${key}-error`).innerHTML = 'This is required field!';
                return;
            }
            clinic[key] = value;
        }

        clinic.address = address;
        const clinicId = form.getAttribute('data-id') || null;
        
        if (clinicId) {
            await updateClinic(clinicId, clinic);
        } else {
            await addClinic(clinic);
        }
    });
})();
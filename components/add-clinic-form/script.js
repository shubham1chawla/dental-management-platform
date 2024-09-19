(function () {
    document.querySelector('#add-client-form').addEventListener('submit', (e) => {
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
        clinic.phone_number = '+1' + clinic.phone_number.replaceAll(' ', '');

        // Loading state
        const button = document.querySelector('#submit-button');
        button.setAttribute('disabled', true);

        fetch('/api/clinics/add', {
            body: JSON.stringify(clinic),
            method: 'POST',
            headers: new Headers({ 'content-type': 'application/json' }),
        }).then((response) => {
            if (response.status !== 200) {
                const alert = document.createElement('div');
                alert.className = 'alert alert-danger mt-4';
                alert.role = 'alert';
                alert.innerHTML = 'An error occured while saving the clinic. Please try again later';
                document.querySelector('#add-client-form').appendChild(alert);
                console.log(alert);
    
                button.setAttribute('disabled', false);
                return;
            }
            window.location.pathname = '/clinics';
        });
    });
})();
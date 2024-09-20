(function () {
    const form = document.querySelector('#add-doctor-form');
    if (!form) return;

    // Load specialties
    const loadSpecialties = async () => {
        const response = await fetch('/api/procedures/list');
        const procedures = await response.json();
        const specialtiesSelect = document.querySelector('#specialties-select');
        for (const procedure of procedures) {
            const option = document.createElement('option');
            option.value = procedure.id
            option.innerText = procedure.name
            specialtiesSelect.appendChild(option);
        }
        const specialtiesError = document.querySelector('#specialties-error');
        specialtiesError.innerHTML = '';

        const submitButton = document.querySelector('#submit-button');
        submitButton.removeAttribute('disabled');
    }
    loadSpecialties();

    form.addEventListener('submit', (e) => {
        e.preventDefault();

        const doctor = {
            npi: null,
            name: null,
            email: null,
            phone_number: null,
            specialties: [],
        };

        for (const key of Object.keys(doctor)) {
            if (key === 'specialties') continue;
            const { value } = document.querySelector(`#${key}-input`);
            if (!value || !value.length) {
                document.querySelector(`${key}-error`).innerHTML = 'This is required field!';
                return;
            }
            doctor[key] = value;
        }

        const options = document.querySelectorAll('#specialties-select > option');
        for (const option of options) {
            if (option.selected) {
                doctor.specialties.push(option.value);
            }
        }

        doctor.npi = parseInt(doctor.npi);
        doctor.phone_number = '+1' + doctor.phone_number.replaceAll(' ', '');
        

        // Loading state
        const button = document.querySelector('#submit-button');
        button.setAttribute('disabled', true);

        fetch('/api/doctors/add', {
            body: JSON.stringify(doctor),
            method: 'POST',
            headers: new Headers({ 'content-type': 'application/json' }),
        }).then((response) => {
            if (response.status !== 200) {
                const alert = document.createElement('div');
                alert.className = 'alert alert-danger mt-4';
                alert.role = 'alert';
                alert.innerHTML = 'An error occured while saving the doctor. Please try again later';
                form.appendChild(alert);   
                button.removeAttribute('disabled');
                return;
            }
            window.location.pathname = '/doctors';
        });
    });
})();
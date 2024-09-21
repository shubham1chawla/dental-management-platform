(function () {
    const form = document.querySelector('#doctor-form');
    if (!form) return;

    // Load specialties
    const loadSpecialties = async (doctorId) => {
        // Loading doctor's specialties
        const doctorSpecialtyIds = new Set();
        if (doctorId) {
            const response = await fetch(`/api/doctors/${doctorId}/specialties/list`);
            const specialties = await response.json();
            specialties.forEach(({id}) => doctorSpecialtyIds.add(id));
        }

        // Adding procedures to options
        const response = await fetch('/api/procedures/list');
        const procedures = await response.json();
        const specialtiesSelect = document.querySelector('#specialties-select');
        for (const procedure of procedures) {
            const option = document.createElement('option');
            option.value = procedure.id
            option.innerText = procedure.name
            if (doctorSpecialtyIds.has(procedure.id)) {
                option.selected = true;
            }
            specialtiesSelect.appendChild(option);
        }
        const specialtiesError = document.querySelector('#specialties-error');
        specialtiesError.innerHTML = '';

        const submitButton = document.querySelector('#submit-button');
        submitButton.removeAttribute('disabled');
    }

    const button = document.querySelector('#submit-button');
    const doctorId = form.getAttribute('data-id') || null;
    loadSpecialties(doctorId);

    const addErrorMessage = () => {
        const alert = document.createElement('div');
        alert.className = 'alert alert-danger mt-4';
        alert.role = 'alert';
        alert.innerHTML = 'An error occured while saving the doctor. Please try again later';
        form.appendChild(alert);   
        button.removeAttribute('disabled');
    }

    const addDoctor = async (doctor) => {
        const response = await fetch('/api/doctors/add', {
            body: JSON.stringify(doctor),
            method: 'POST',
            headers: new Headers({ 'content-type': 'application/json' }),
        });
        if (response.ok) {
            window.location.pathname = '/doctors';
            return;
        }
        addErrorMessage();
    }

    const updateDoctor = async (doctorId, doctor) => {
        const response = await fetch(`/api/doctors/${doctorId}/update`, {
            body: JSON.stringify(doctor),
            method: 'PUT',
            headers: new Headers({ 'content-type': 'application/json' }),
        });
        if (response.ok) {
            window.location.pathname = `/doctors/${doctorId}`;
            return;
        }
        addErrorMessage();
    }

    form.addEventListener('submit', (e) => {
        e.preventDefault();
        button.setAttribute('disabled', true);

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

        if (doctorId) {
            updateDoctor(doctorId, doctor);
        } else {
            addDoctor(doctor);
        }
    });
})();
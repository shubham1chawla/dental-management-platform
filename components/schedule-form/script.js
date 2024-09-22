(function() {
    const form = document.querySelector('#schedule-form');
    if (!form) return;

    const patientId = form.getAttribute('data-id');
    
    const procedureSelect = form.querySelector('#procedure-select');
    const clinicSelect = form.querySelector('#clinic-select');
    const doctorSelect = form.querySelector('#doctor-select');
    const dateInput = form.querySelector('#date-input');
    const slotSelect = form.querySelector('#slot-select');
    const submitButton = form.querySelector('#submit-button');

    const addErrorMessage = () => {
        const alert = document.createElement('div');
        alert.className = 'alert alert-danger mt-4';
        alert.role = 'alert';
        alert.innerHTML = 'An error occured while saving the appointment. Please try again later';
        form.appendChild(alert);
    }

    const showSubmitButton = () => {
        submitButton.classList.remove('visually-hidden');
        submitButton.removeAttribute('disabled');
    };

    const hideSubmitButton = () => {
        submitButton.classList.add('visually-hidden');
        submitButton.setAttribute('disabled', true);
    };

    const showLoading = (fieldId) => {
        const fieldNode = form.querySelector(fieldId);
        const loadingNode = fieldNode.querySelector('span#loading');
        loadingNode.classList.remove('visually-hidden');
    }

    const hideLoading = (fieldId) => {
        const fieldNode = form.querySelector(fieldId);
        const loadingNode = fieldNode.querySelector('span#loading');
        loadingNode.classList.add('visually-hidden');
    }

    const showUnavailable = (fieldId) => {
        const fieldNode = form.querySelector(fieldId);
        const unavailableNode = fieldNode.querySelector('span#unavailable');
        unavailableNode.classList.remove('visually-hidden');
    }

    const hideUnavailable = (fieldId) => {
        const fieldNode = form.querySelector(fieldId);
        const unavailableNode = fieldNode.querySelector('span#unavailable');
        unavailableNode.classList.add('visually-hidden');
    }
    
    const resetFields = (fieldIds) => {
        fieldIds.forEach((id) => {
            const fieldNode = form.querySelector(id);
            fieldNode.classList.add('visually-hidden');
        });
    }

    const showFields = (fieldIds) => {
        fieldIds.forEach((id) => {
            const node = form.querySelector(id);
            node.classList.remove('visually-hidden');
        });
    }

    const clearOptions = (selectNode) => {
        for (const option of selectNode.querySelectorAll('option')) {
            if (!!option.value) {
                selectNode.removeChild(option);
            } else {
                option.selected = true;
            }
        }
    };

    const disableAllFields = () => {
        [
            procedureSelect, 
            clinicSelect, 
            doctorSelect, 
            dateInput, 
            slotSelect, 
            submitButton
        ].forEach((node) => node.setAttribute('disabled', true));
    };

    const setClinics = async () => {       
        const procedureId = procedureSelect.value;
        const response = await fetch(`/api/procedures/${procedureId}/clinics/list`);
        const clinics = await response.json();
        if (!clinics || !clinics.length) {
            return false;
        }

        for (const clinic of clinics) {
            const option = document.createElement('option');
            option.value = clinic.id;
            option.innerText = clinic.name;
            clinicSelect.appendChild(option);
        }
        return true;
    };

    const setDoctors = async () => {
        const procedureId = procedureSelect.value;
        const clinicId = clinicSelect.value;
        const response = await fetch(`/api/procedures/${procedureId}/clinics/${clinicId}/doctors/list`);
        const doctors = await response.json();
        if (!doctors || !doctors.length) {
            return false;
        }

        for (const doctor of doctors) {
            const option = document.createElement('option');
            option.value = doctor.id;
            option.innerText = doctor.name;
            doctorSelect.appendChild(option);
        }
        return true;
    }

    const setAppointmentSlots = async () => {
        const clinicId = clinicSelect.value;
        const doctorId = doctorSelect.value;
        const date = dateInput.value;
        const response = await fetch(`/api/clinics/${clinicId}/doctors/${doctorId}/schedules/${date}/slots/list`);
        const slots = await response.json();
        if (!slots || !slots.length) {
            return false;
        }

        for (const slot of slots) {
            const option = document.createElement('option');
            option.value = `${slot.start_time};${slot.end_time}`;
            option.innerText = `${slot.start_time} - ${slot.end_time}`;
            option.disabled = slot.booked;
            slotSelect.appendChild(option);
        }
        return true;
    }

    procedureSelect.addEventListener('change', async () => {
        resetFields(['#clinic-field', '#doctor-field', '#date-field', '#slot-field']);
        showFields(['#clinic-field']);
        clearOptions(clinicSelect);
        showLoading('#clinic-field');
        hideUnavailable('#clinic-field');
        const added = await setClinics();
        if (!added) {
            showUnavailable('#clinic-field');
        }
        hideLoading('#clinic-field');
        hideSubmitButton();
    });

    clinicSelect.addEventListener('change', async () => {
        resetFields(['#doctor-field', '#date-field', '#slot-field']);
        showFields(['#doctor-field']);
        clearOptions(doctorSelect);
        showLoading('#doctor-field');
        hideUnavailable('#doctor-field');
        const added = await setDoctors();
        if (!added) {
            showUnavailable('#doctor-field');
        }
        hideLoading('#doctor-field');
        hideSubmitButton();
    });

    doctorSelect.addEventListener('change', () => {
        resetFields(['#date-field', '#slot-field']);
        showFields(['#date-field']);
        dateInput.value = '';
        hideSubmitButton();
    });

    dateInput.addEventListener('change', async () => {
        resetFields(['#slot-field']);
        showFields(['#slot-field']);
        clearOptions(slotSelect);
        showLoading('#slot-field');
        hideUnavailable('#slot-field');
        const added = await setAppointmentSlots();
        if (!added) {
            showUnavailable('#slot-field');
        }
        hideLoading('#slot-field');
        hideSubmitButton();
    });

    slotSelect.addEventListener('change', () => {
        showSubmitButton();
    });

    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        disableAllFields();
        
        const [start_time, end_time] = slotSelect.value.split(';');
        const appointment = {
            procedure_id: parseInt(procedureSelect.value),
            clinic_id: parseInt(clinicSelect.value),
            doctor_id: parseInt(doctorSelect.value),
            date: dateInput.value,
            start_time,
            end_time,
        };

        const response = await fetch(`/api/patients/${patientId}/appointments/add`, {
            body: JSON.stringify(appointment),
            method: 'POST',
            headers: new Headers({ 'content-type': 'application/json' }),
        });
        if (response.ok) {
            window.location.pathname = `/patients/${patientId}`;
            return;
        }
        addErrorMessage();
    });
})();

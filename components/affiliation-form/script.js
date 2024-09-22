(function () {
    const form = document.querySelector('#affiliation-form');
    if (!form) return;

    const clinicId = form.getAttribute('data-id');
    const doctorSelect = form.querySelector('#doctor-select');
    const button = form.querySelector('#submit-button');

    const FIELDS_LOOKUP = {
        'street_address_1': (schedule) => schedule.office_address.street_address_1,
        'street_address_2': (schedule) => schedule.office_address.street_address_2,
        'city': (schedule) => schedule.office_address.city,
        'state': (schedule) => schedule.office_address.state,
        'zipcode': (schedule) => schedule.office_address.zipcode,
        'start_time': (schedule) => schedule.start_time,
        'end_time': (schedule) => schedule.end_time,
    };

    const addErrorMessage = () => {
        const alert = document.createElement('div');
        alert.className = 'alert alert-danger mt-4';
        alert.role = 'alert';
        alert.innerHTML = 'Some requests were not processed. Please refresh and try again later.';
        form.appendChild(alert);
        button.removeAttribute('disabled');
    }

    const showLoadingSchedule = () => {
        const node = form.querySelector('#loading');
        node.classList.remove('visually-hidden');
    };

    const hideLoadingSchedule = () => {
        const node = form.querySelector('#loading');
        node.classList.add('visually-hidden');
    };

    const disableFields = (weekday) => {
        const scheduleNode = form.querySelector(`#schedule-${weekday}`);
        for (const field of Object.keys(FIELDS_LOOKUP)) {
            const node = scheduleNode.querySelector(`#${field}-input`);
            node.setAttribute('disabled', true);
        }
    }

    const enableFields = (weekday) => {
        const scheduleNode = form.querySelector(`#schedule-${weekday}`);
        for (const field of Object.keys(FIELDS_LOOKUP)) {
            const node = scheduleNode.querySelector(`#${field}-input`);
            node.removeAttribute('disabled');
        }
    }

    const resetFields = () => {
        for (let i = 0; i < 5; i++) {
            disableFields(i);
        }
    }

    const enableRemoveOperation = (weekday) => {
        const removeOperation = form.querySelector(`#schedule-${weekday}-operation-remove`);
        removeOperation.removeAttribute('disabled');
    }

    const resetRemoveOperations = () => {
        for (let i = 0; i < 5; i++) {
            const removeOperation = form.querySelector(`#schedule-${i}-operation-remove`);
            removeOperation.setAttribute('disabled', true);
        }
    }

    const disableAddEditOperation = (weekday) => {
        const addEditOperation = form.querySelector(`#schedule-${weekday}-operation-add-edit`);
        addEditOperation.setAttribute('disabled', true);
    }

    const resetAddEditOperations = () => {
        for (let i = 0; i < 5; i++) {
            const addEditOperation = form.querySelector(`#schedule-${i}-operation-add-edit`);
            addEditOperation.removeAttribute('disabled');
        }
    }

    const resetUnchangedOperations = () => {
        for (let i = 0; i < 5; i++) {
            const unchangedOperation = form.querySelector(`#schedule-${i}-operation-unchanged`);
            unchangedOperation.checked = true;
        }
    }

    const showRemoveAlert = (weekday) => {
        const node = form.querySelector(`#schedule-${weekday}-alert-remove`);
        node.classList.remove('visually-hidden');
    }

    const hideRemoveAlert = (weekday) => {
        const node = form.querySelector(`#schedule-${weekday}-alert-remove`);
        node.classList.add('visually-hidden');
    }

    const setBadge = (weekday, text, classes) => {
        const badgeNode = form.querySelector(`#schedule-${weekday}-badge`);
        badgeNode.classList.add(classes);
        badgeNode.innerHTML = text;
    }

    const resetBadge = () => {
        for (let i = 0; i < 5; i++) {
            const badgeNode = form.querySelector(`#schedule-${i}-badge`);
            badgeNode.setAttribute('class', 'badge');
            badgeNode.innerHTML = '';
        }
    }

    const setSchedule = (weekday, schedule) => {
        const scheduleNode = form.querySelector(`#schedule-${weekday}`);
        scheduleNode.classList.remove('visually-hidden');

        // Setting up data-id field
        if (schedule) {
            scheduleNode.setAttribute('data-id', schedule.id);
            setBadge(weekday, 'Schedule Exists', 'text-bg-success');
        }

        // Enabling and setting fields
        for (const field of Object.keys(FIELDS_LOOKUP)) {
            const node = scheduleNode.querySelector(`#${field}-input`);
            if (schedule) {
                node.value = FIELDS_LOOKUP[field](schedule);
                enableRemoveOperation(weekday);
            }
        }
    }

    const setDoctorSchedule = async () => {
        showLoadingSchedule();
        const doctorId = doctorSelect.value;

        const [clinicSchedulesResponse, doctorSchedulesResponse] = await Promise.all([
            fetch(`/api/clinics/${clinicId}/doctors/${doctorId}/schedules/list`),
            fetch(`/api/doctors/${doctorId}/schedules/list`),
        ]);

        const [clinicSchedules, doctorSchedules] = await Promise.all([
            clinicSchedulesResponse.json(),
            doctorSchedulesResponse.json(),
        ]);

        // Creating a map of doctor's schedule for current clinic
        const clinicScheduleMap = new Map();
        for (const clinicSchedule of clinicSchedules) {
            clinicScheduleMap.set(clinicSchedule.weekday, clinicSchedule);
        }

        // Creating a map of doctor's schedule different from current clinic
        const doctorScheduleMap = new Map();
        for (const doctorSchedule of doctorSchedules) {
            if (doctorSchedule.clinic_id !== parseInt(clinicId)) {
                doctorScheduleMap.set(doctorSchedule.weekday, doctorSchedule);
            }
        }

        for (let i = 0; i < 5; i++) {
            setSchedule(i, clinicScheduleMap.get(i));

            // Checking if doctor already working at some other clinic
            if (doctorScheduleMap.has(i)) {
                disableAddEditOperation(i);
                setBadge(i, 'Doctor Unavailable', 'text-bg-danger');
            }
        }

        hideLoadingSchedule();
    };

    if (doctorSelect.value) {
        setDoctorSchedule();
    } else {
        hideLoadingSchedule();
        doctorSelect.addEventListener('change', () => {
            resetBadge();
            resetRemoveOperations();
            resetAddEditOperations();
            resetUnchangedOperations();
            resetFields();
            setDoctorSchedule();
        });
    }

    // Setting operations interactivity
    for (let i = 0; i < 5; i++) {
        const unchangedOperation = form.querySelector(`#schedule-${i}-operation-unchanged`);
        unchangedOperation.addEventListener('change', (e) => {
            if (e.target.checked) {
                hideRemoveAlert(i);
                disableFields(i);
            }
        });

        const addEditOperation = form.querySelector(`#schedule-${i}-operation-add-edit`);
        addEditOperation.addEventListener('change', (e) => {
            if (e.target.checked) {
                hideRemoveAlert(i);
                enableFields(i);
            }
        });

        const removeOperation = form.querySelector(`#schedule-${i}-operation-remove`);
        removeOperation.addEventListener('change', (e) => {
            if (e.target.checked) {
                showRemoveAlert(i);
                disableFields(i);
            }
        });
    }

    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        button.setAttribute('disabled', true);

        const addSchedules = [];
        const updateSchedules = {};
        const removeSchedules = [];
        for (let i = 0; i < 5; i++) {
            const scheduleNode = form.querySelector(`#schedule-${i}`);
            const scheduleId = scheduleNode.getAttribute('data-id') || null;

            // Ignoring unchanged schedules
            if (form.querySelector(`#schedule-${i}-operation-unchanged`).checked) {
                continue;
            }

            // Checking if the schedule is to be removed
            if (scheduleId && form.querySelector(`#schedule-${i}-operation-remove`).checked) {
                removeSchedules.push(scheduleId);
                continue;
            }

            const schedule = {
                office_address: {
                    street_address_1: scheduleNode.querySelector(`#street_address_1-input`).value,
                    street_address_2: scheduleNode.querySelector(`#street_address_2-input`).value,
                    city: scheduleNode.querySelector(`#city-input`).value,
                    state: scheduleNode.querySelector(`#state-input`).value,
                    zipcode: scheduleNode.querySelector(`#zipcode-input`).value,
                },
                start_time: scheduleNode.querySelector(`#start_time-input`).value,
                end_time: scheduleNode.querySelector(`#end_time-input`).value,
                weekday: i,
            };

            // Checking whether to add or edit schedule
            if (scheduleId) {
                updateSchedules[scheduleId] = schedule;
            } else {
                addSchedules.push(schedule);
            }
        }

        const doctorId = doctorSelect.value;
        const responses = await Promise.all([
            ...removeSchedules.map(
                (scheduleId) => fetch(`/api/clinics/${clinicId}/doctors/${doctorId}/schedules/${scheduleId}/remove`, {
                    method: 'DELETE',
                }),
            ),
            ...Object.keys(updateSchedules).map(
                (scheduleId) => fetch(`/api/clinics/${clinicId}/doctors/${doctorId}/schedules/${scheduleId}/update`, {
                    method: 'PUT',
                    body: JSON.stringify(updateSchedules[scheduleId]),
                    headers: new Headers({ 'content-type': 'application/json' }),
                }),
            ),
            ...addSchedules.map(
                (schedule) => fetch(`/api/clinics/${clinicId}/doctors/${doctorId}/schedules/add`, {
                    method: 'POST',
                    body: JSON.stringify(schedule),
                    headers: new Headers({ 'content-type': 'application/json' }),
                }),
            ),
        ]);

        if (responses.every((response) => response.ok)) {
            window.location.pathname = `/clinics/${clinicId}`;
            return;
        }

        // Error condition
        addErrorMessage();
    });
})();
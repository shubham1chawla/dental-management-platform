(async function() {
    const setLastVisitDetails = async (patientId) => {
        const appointmentsResponse = await fetch(`/api/patients/${patientId}/appointments/last`);
        const appointments = await appointmentsResponse.json();
        
        const dateNode = document.querySelector(`#last-visit-date-${patientId}`);
        const doctorNode = document.querySelector(`#last-visit-doctor-${patientId}`);
        const proceduresNode = document.querySelector(`#last-visit-procedures-${patientId}`);
        if (!appointments || !appointments.length) {
            dateNode.innerHTML = `<span class="text-danger">No visit found</span>`;
            doctorNode.innerHTML = `<span class="text-danger">No visit found</span>`;
            proceduresNode.innerHTML = `<span class="text-danger">No visit found</span>`;
            return;
        }

        const lastAppointment = appointments[0];
        dateNode.innerHTML = `<span class="text-primary">
            Last Visit Date: ${lastAppointment.date}
        </span>`;
        doctorNode.innerHTML = `<span class="text-primary">
            Last Visit Doctor: ${lastAppointment.doctor.name}
        </span>`;

        // Getting appointment procedures
        const proceduresResponse = await fetch(`/api/appointments/${lastAppointment.id}/procedures/list`);
        const procedures = await proceduresResponse.json()
        proceduresNode.innerHTML = `<span class="text-primary">
            Last Visit Procedures: ${procedures.map(({name}) => name).join(', ')}
        </span>`;
    }

    const setNextVisitDetails = async (patientId) => {
        const appointmentsResponse = await fetch(`/api/patients/${patientId}/appointments/next`);
        const appointments = await appointmentsResponse.json();
        
        const dateNode = document.querySelector(`#next-visit-date-${patientId}`);
        const doctorNode = document.querySelector(`#next-visit-doctor-${patientId}`);
        const proceduresNode = document.querySelector(`#next-visit-procedures-${patientId}`);
        if (!appointments || !appointments.length) {
            dateNode.innerHTML = `<span class="text-danger">No visit found</span>`;
            doctorNode.innerHTML = `<span class="text-danger">No visit found</span>`;
            proceduresNode.innerHTML = `<span class="text-danger">No visit found</span>`;
            return;
        }

        const nextAppointment = appointments[0];
        dateNode.innerHTML = `<span class="text-success">
            Next Visit Date: ${nextAppointment.date}
        </span>`;
        doctorNode.innerHTML = `<span class="text-success">
            Next Visit Doctor: ${nextAppointment.doctor.name}
        </span>`;

        // Getting appointment procedures
        const proceduresResponse = await fetch(`/api/appointments/${nextAppointment.id}/procedures/list`);
        const procedures = await proceduresResponse.json()
        proceduresNode.innerHTML = `<span class="text-success">
            Next Visit Procedures: ${procedures.map(({name}) => name).join(', ')}
        </span>`;
    }

    // Loading patients details
    const patientCards = document.querySelectorAll('.patient-card');
    for (const card of patientCards) {
        const patientId = card.getAttribute('data-id');
        await Promise.all([
            setLastVisitDetails(patientId),
            setNextVisitDetails(patientId),
        ]);
    }
})();
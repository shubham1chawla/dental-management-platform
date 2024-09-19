(async function () {
    const setSpecialties = async (doctorId) => {
        const response = await fetch(`/api/doctors/${doctorId}/specialties/list`);
        const specialties = await response.json();
        document.querySelector(`#specialties-${doctorId}`).innerHTML = `${specialties.map(({ name }) => name).join(', ')}`;
    }

    const setAffiliatedClinics = async (doctorId) => {
        const response = await fetch(`/api/doctors/${doctorId}/clinics/list`);
        const clinics = await response.json();
        document.querySelector(`#clinics-count-${doctorId}`).innerHTML = `Affiliated Clinics: ${clinics.length}`;
    };

    const setAffiliatedPatients = async (doctorId) => {
        const response = await fetch(`/api/doctors/${doctorId}/patients/list`);
        const patients = await response.json();
        document.querySelector(`#patients-count-${doctorId}`).innerHTML = `Affiliated Patients: ${patients.length}`;
    };

    // Loading clinics' number of affiliations using APIs
    const doctorCards = document.querySelectorAll('.doctor-card');
    if (doctorCards.length) {
        for (const card of doctorCards) {
            const doctorId = card.getAttribute('data-id');
            await Promise.all([
                setSpecialties(doctorId),
                setAffiliatedClinics(doctorId),
                setAffiliatedPatients(doctorId),
            ]);
        }
    }
})();
(async function () {
    const setAffiliatedClinics = async (doctorId) => {
        const response = await fetch(`/api/doctors/${doctorId}/clinics/list`);
        const clinics = await response.json();
        document.querySelector(`#clinics-count-${doctorId}`).innerHTML = `Affiliated Clinics: ${clinics.length}`
    };

    const setAffiliatedPatients = async (doctorId) => {
        const response = await fetch(`/api/doctors/${doctorId}/patients/list`);
        const patients = await response.json();
        document.querySelector(`#patients-count-${doctorId}`).innerHTML = `Affiliated Patients: ${patients.length}`
    };

    // Loading clinics' number of affiliations using APIs
    const doctorCards = document.querySelectorAll('.doctor-card');
    if (doctorCards.length) {
        for (const card of doctorCards) {
            const doctorId = card.getAttribute('data-id');
            await Promise.all([
                setAffiliatedClinics(doctorId),
                setAffiliatedPatients(doctorId),
            ]);
        }
    }
})();
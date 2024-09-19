(async function () {
    const setAffiliatedDoctors = async (clinicId) => {
        const response = await fetch(`/api/clinics/${clinicId}/doctors/list`);
        const doctors = await response.json();
        document.querySelector(`#doctors-count-${clinicId}`).innerHTML = `Affiliated Doctors: ${doctors.length}`
    };

    const setAffiliatedPatients = async (clinicId) => {
        const response = await fetch(`/api/clinics/${clinicId}/patients/list`);
        const patients = await response.json();
        document.querySelector(`#patients-count-${clinicId}`).innerHTML = `Affiliated Patients: ${patients.length}`
    };

    // Loading clinics' number of affiliations using APIs
    const clinicCards = document.querySelectorAll('.clinic-card');
    if (clinicCards.length) {
        for (const card of clinicCards) {
            const clinicId = card.getAttribute('data-id');
            await Promise.all([
                setAffiliatedDoctors(clinicId),
                setAffiliatedPatients(clinicId),
            ]);
        }
    }
})();
(async function() {
    // Loading appointment details
    const appointmentCards = document.querySelectorAll('.appointment-card');
    for (const card of appointmentCards) {
        const appointmentId = card.getAttribute('data-id');
        
        const response = await fetch(`/api/appointments/${appointmentId}/procedures/list`);
        const procedures = await response.json();

        const node = document.querySelector(`#procedures-${appointmentId}`);
        node.innerHTML = procedures.map(({name}) => name).join(', ');
    }
})();
(async function () {

    const getWeekdaySchedule = (schedules) => {
        const weekdaySchedules = new Map();
        for (const schedule of schedules) {
            if (!weekdaySchedules.has(schedule.weekday)) {
                weekdaySchedules.set(schedule.weekday, []);
            }
            weekdaySchedules.get(schedule.weekday).push(schedule);
        }
        return weekdaySchedules;
    }

    const formatOfficeAddress = (office_address) => {
        let address = [`${office_address.street_address_1},`];
        if (office_address.street_address_2) {
            address.push(office_address.street_address_2)
        }
        address.push(office_address.city, office_address.state, office_address.zipcode);
        return address.join(' ');
    }

    const doctorCards = document.querySelectorAll('.doctor-clinic-card');
    if (doctorCards.length) {
        for (const card of doctorCards) {
            const doctorId = card.getAttribute('data-doctor-id');
            const clinicId = card.getAttribute('data-id');

            const response = await fetch(`/api/clinics/${clinicId}/doctors/${doctorId}/schedules/list`);
            const schedules = await response.json();
            
            const weekdaySchedules = getWeekdaySchedule(schedules);
            
            // Iterating over all the ISO week days Monday - Friday
            for (let i = 0; i < 5; i++) {
                const node = card.querySelector(`#schedule-${doctorId}-${i}`);
                if (!weekdaySchedules.has(i)) {
                    node.innerHTML = '<span class="text-danger"><i class="bi bi-ban"></i> No schedule found</span>';
                    continue;
                }
                node.innerHTML = '';

                const doctorWeekdaySchedules = weekdaySchedules.get(i);
                for (const doctorWeekdaySchedule of doctorWeekdaySchedules) {
                    const { office_address, start_time, end_time } = doctorWeekdaySchedule;
                    const element = document.createElement('span');
                    element.innerHTML = `
                        <span class="text-success">
                            <i class="bi bi-geo-alt-fill"></i> Office: ${formatOfficeAddress(office_address)}
                        </span>
                        <br />
                        <span class="text-success">
                            <i class="bi bi-clock"></i> ${start_time} - ${end_time}
                        </span>
                    `
                    node.appendChild(element);
                }
            }
        }
    }
})();
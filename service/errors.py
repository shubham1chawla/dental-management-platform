class NoClinicFoundError(RuntimeError):
    def __init__(self, clinic_id: int):
        super().__init__(f'No clinic associated with id {clinic_id}')


class NoDoctorFoundError(RuntimeError):
    def __init__(self, doctor_id: int):
        super().__init__(f'No doctor associated with id {doctor_id}')


class NoPatientFoundError(RuntimeError):
    def __init__(self, patient_id: int):
        super().__init__(f'No patient associated with id {patient_id}')


class NoProcedureFoundError(RuntimeError):
    def __init__(self, procedure_id: int):
        super().__init__(f'No procedure associated with id {procedure_id}')


class NoDoctorScheduleFoundError(RuntimeError):
    def __init__(self, schedule_id: int):
        super().__init__(f'No schedule associated with id {schedule_id}')


class DoctorUnavailableError(RuntimeError):
    def __init__(self, doctor_id: int, weekday: int):
        super().__init__(f'Doctor associated with {doctor_id} already assigned to another clinic for weekday {weekday}')

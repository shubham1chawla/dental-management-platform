class NoClinicFoundError(RuntimeError):
    def __init__(self, clinic_id: int):
        super().__init__(f'No clinic associated with id {clinic_id}')


class NoDoctorFoundError(RuntimeError):
    def __init__(self, doctor_id: int):
        super().__init__(f'No doctor associated with id {doctor_id}')


class NoPatientFoundError(RuntimeError):
    def __init__(self, patient_id: int):
        super().__init__(f'No patient associated with id {patient_id}')

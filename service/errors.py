class NoClinicFoundError(RuntimeError):
    def __init__(self, clinic_id: int):
        super().__init__(f'No clinic associated with id {clinic_id}')

class NoDoctorFoundError(RuntimeError):
    def __init__(self, doctor_id: int):
        super().__init__(f'No doctor associated with id {doctor_id}')

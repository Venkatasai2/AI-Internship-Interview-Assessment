import heapq
from datetime import datetime, timedelta
import random

class Doctor:
    def __init__(self, doctor_id, availability_blocks, prefers_walk_ins=False):
        self.doctor_id = doctor_id
        self.queue = []
        self.availability_blocks = availability_blocks  # Example: [(9, 12), (15, 18)]
        self.prefers_walk_ins = prefers_walk_ins  # Here i added Doctor preference for walk-ins
    
    def add_patient(self, patient):
        heapq.heappush(self.queue, (patient.priority, patient.patient_id, patient))
    
    def next_patient(self):
        if self.queue:
            return heapq.heappop(self.queue)[2]  # Extract patient object
        return None

class Patient:
    def __init__(self, patient_id, arrival_time, scheduled_time, urgency, source):
        self.patient_id = patient_id
        self.arrival_time = arrival_time
        self.scheduled_time = scheduled_time
        self.urgency = urgency
        self.source = source  # 'App', 'Walk-in', 'WhatsApp', etc.
        self.priority = self.calculate_priority()

    def calculate_priority(self):
        """
        Priority formula:
        - Higher urgency -> Higher priority
        - Delay in arrival decreases priority
        - Walk-ins might be deprioritized if doctor prefers scheduled appointments
        """
        delay = max(0, (self.arrival_time - self.scheduled_time).total_seconds() // 60)
        priority = self.urgency * 10 - delay
        if self.source == "Walk-in":
            priority -= 5  # Slightly lower priority for walk-ins unless the doctor prefers them
        return priority

class QueueManagementSystem:
    def __init__(self):
        self.doctors = {}

    def add_doctor(self, doctor_id, availability_blocks, prefers_walk_ins=False):
        self.doctors[doctor_id] = Doctor(doctor_id, availability_blocks, prefers_walk_ins)

    def assign_patient(self, doctor_id, patient):
        if doctor_id in self.doctors:
            doctor = self.doctors[doctor_id]
            if patient.source == "Walk-in" and not doctor.prefers_walk_ins:
                patient.priority -= 3  # Here I added Further deprioritize walk-ins for doctors who prefer scheduled patients
            doctor.add_patient(patient)

    def estimate_wait_time(self, doctor_id):
        if doctor_id not in self.doctors:
            return -1  # Return -1 if the doctor ID does not exist
        
        num_patients = len(self.doctors[doctor_id].queue)
        if num_patients == 0:
            return 0  # No waiting time if no patients are in queue
        
        avg_consult_time = random.randint(8, 22)  # Simulating doctor-specific consultation times
        return num_patients * avg_consult_time

# Example Usage
qms = QueueManagementSystem()
qms.add_doctor(1, [(9, 12), (15, 18)], prefers_walk_ins=False)

patient1 = Patient(101, datetime.now(), datetime.now() + timedelta(minutes=15), urgency=2, source="App")
patient2 = Patient(102, datetime.now(), datetime.now() + timedelta(minutes=10), urgency=3, source="Walk-in")

qms.assign_patient(1, patient1)
qms.assign_patient(1, patient2)

print(f"Estimated wait time for Doctor 1: {qms.estimate_wait_time(1)} minutes")

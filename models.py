""" ORM Models for a patient database.  Also includes code to build the database if it doesn't exist.


Author: Tyler Baker
Class: CSI-260-01
Assignment: Database Lab

Certification of Authenticity:
I certify that this is entirely my own work, except where I have given
fully-documented references to the work of others. I understand the definition
and consequences of plagiarism and acknowledge that the assessor of this
assignment may, for the purpose of assessing this assignment:
- Reproduce this assignment and provide a copy to another member of academic
- staff; and/or Communicate a copy of this assignment to a plagiarism checking
- service (which may then retain a copy of this assignment on its database for
- the purpose of future plagiarism checking)
"""
import peewee as db


database = db.SqliteDatabase("patient_database.sqlite")


class Procedure(db.Model):
    """ORM model of procedures table."""
    name = db.CharField()
    min_cost = db.DecimalField(default=None)
    max_cost = db.DecimalField(default=None)
    pre_procedure_checklist = db.TextField(default='')

    class Meta:
        table_name = 'procedures'
        database = database

    def __str__(self):
        return f'{self.name}'

    def all_info(self):
        to_return = f'Procedure {self.id}: {str(self)}'
        if self.min_cost and self.max_cost:
            to_return += f'\n    ${self.min_cost} - ${self.max_cost}'
        if self.pre_procedure_checklist != '':
            to_return += f'\n    {self.pre_procedure_checklist}'
        return to_return


class Doctor(db.Model):
    """ORM model of doctors table."""
    first_name = db.CharField()
    last_name = db.CharField()
    primary_office = db.CharField(default='')

    class Meta:
        table_name = 'doctors'
        database = database

    def __str__(self):
        return f'Dr. {self.first_name} {self.last_name}'

    def all_info(self):
        to_return = f'Doctor {self.id}: {str(self)}'
        if self.primary_office != '':
            to_return += f'\n    Primary Office: {self.primary_office}'
        return to_return


class Patient(db.Model):
    """ORM model of patients table."""
    first_name = db.CharField()
    last_name = db.CharField()
    address = db.CharField(default='')
    phone_number = db.CharField(default='')
    emergency_contact = db.CharField(default='')
    emergency_phone = db.CharField(default='')
    primary_care_doctor = db.ForeignKeyField(Doctor, backref='patients', null=True, default=None)

    class Meta:
        table_name = 'patients'
        database = database

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    def all_info(self):
        to_return = f'Patient {self.id}: {str(self)}'
        if self.address != '':
            to_return += f'\n    Address: {self.address}'
        if self.phone_number != '':
            to_return += f'\n    Phone Number: {self.phone_number}'
        if self.emergency_contact != '':
            to_return += f'\n    Emergency Contact: {self.emergency_contact}'
        if self.emergency_phone != '':
            to_return += f'\n    Emergency Phone: {self.emergency_phone}'
        if self.primary_care_doctor != '':
            to_return += f'\n    Primary Care Doctor: {self.primary_care_doctor}'
        return to_return


class PerformedProcedure(db.Model):
    """ORM model of performed_procedures table."""
    patient = db.ForeignKeyField(Patient, backref='procedure_history', default=None)
    doctor = db.ForeignKeyField(Doctor, backref='procedure_history', default=None)
    procedure = db.ForeignKeyField(Procedure, backref='procedure_history', default=None)
    procedure_date = db.DateField(default=None)
    notes = db.TextField(default='')

    class Meta:
        table_name = 'performed_procedures'
        database = database

    def __str__(self):
        return f'{self.procedure}'

    def all_info(self):
        to_return = f'Performed Procedure {self.id}: {str(self)}'
        to_return += f'\n    {self.patient}'
        to_return += f'\n    {self.doctor}'
        if self.procedure_date != '':
            to_return += f'\n    Address: {self.procedure_date}'
        if self.notes != '':
            to_return += f'\n    Phone Number: {self.notes}'
        return to_return


class Medication(db.Model):
    """
    ORM model of medications table
    """
    name = db.CharField()
    common_name = db.CharField()
    notes = db.TextField(default='')

    class Meta:
        table_name = 'medications'
        database = database

    def __str__(self):
        return f'{self.name}'

    def all_info(self):
        to_return = f'Medication {self.id}: {str(self)}'
        to_return += f'\n    AKA: {self.common_name}'
        if self.notes != '':
            to_return += f'\n    {self.notes}'
        return to_return


class AssignedMedication(db.Model):
    """ORM model of assigned_medications table."""
    patient = db.ForeignKeyField(Patient, backref='medication_history', default=None)
    medication = db.ForeignKeyField(Medication, backref='medication_history', default=None)
    dosage = db.CharField()
    date_added = db.DateField(default=None)

    class Meta:
        table_name = 'assigned_medications'
        database = database

    def __str__(self):
        return f'{self.medication}'

    def all_info(self):
        to_return = f'Assigned Medication {self.id}: {str(self)}'
        to_return += f'\n    AKA: {self.medication.common_name}'
        to_return += f'\n    Patient: {self.patient}'
        to_return += f'\n    Dosage: {self.dosage}'
        if self.date_added != '':
            to_return += f'\n    Address: {self.date_added}'
        return to_return


if __name__ == "__main__":
    try:
        Procedure.create_table()
    except db.OperationalError:
        print("Procedure table already exists!")

    try:
        Doctor.create_table()
    except db.OperationalError:
        print("Doctor table already exists!")

    try:
        Patient.create_table()
    except db.OperationalError:
        print("Patient table already exists!")

    try:
        PerformedProcedure.create_table()
    except db.OperationalError:
        print("performed_procedures table already exists!")

    try:
        Medication.create_table()
    except db.OperationalError:
        print("performed_procedures table already exists!")

    try:
        AssignedMedication.create_table()
    except db.OperationalError:
        print("performed_procedures table already exists!")

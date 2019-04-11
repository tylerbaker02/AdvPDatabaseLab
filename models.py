import peewee as db
"""
ORM Models for a patient database.  Also includes code to build the database
if it doesn't exist.
"""

database = db.SqliteDatabase("patient_database.sqlite")


class Procedure(db.Model):
    """
    ORM model of procedures table
    """
    name = db.CharField()
    min_cost = db.DecimalField(default=None)
    max_cost = db.DecimalField(default=None)
    pre_procedure_checklist = db.TextField(default='')

    class Meta:
        table_name = 'procedures'
        database = database

    def __str__(self):
        return f'{self.name} (${self.min_cost} - ${self.max_cost})'

    def all_info(self):
        to_return = f'Procedure {self.id}: {str(self)}'
        if self.pre_procedure_checklist != '':
            to_return += f'\n    {self.pre_procedure_checklist}'
        return to_return


class Doctor(db.Model):
    """
    ORM model of doctors table
    """
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
    """
    ORM model of patients table
    """
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
    """
    ORM model of performed_procedures table
    """
    patient = db.ForeignKeyField(Patient, backref='procedure_history')
    doctor = db.ForeignKeyField(Doctor, backref='procedure_history')
    procedure = db.ForeignKeyField(Procedure, backref='procedure_history')
    procedure_date = db.DateField(default=None)
    notes = db.TextField(default='')

    class Meta:
        table_name = 'performed_procedures'
        database = database


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
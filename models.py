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
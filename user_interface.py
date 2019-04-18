"""User Interface for medical database


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

import models as db
import sys

menu = """
1. Add Doctor
2. Add Patient
3. Add Procedure
4. Add Performed Procedure
5. Lookup a patient's medical records
6. Add a medication to the list of available prescriptions
7. Assign a medication to a patient
8. Quit
Choose:
"""


def add_doctor():
    """User Interface for adding a new doctor to the database."""
    params = dict()
    params['first_name'] = input('First Name? ')
    params['last_name'] = input('Last Name? ')
    params['primary_office'] = input('Primary Office? ')
    new_doc = db.Doctor(**params)
    new_doc.save()


def add_patient():
    """User Interface for adding a new patient to the database."""
    params = dict()
    params['first_name'] = input('First Name? ')
    params['last_name'] = input('Last Name? ')
    params['address'] = input('Address? ')
    params['phone_number'] = input('Phone Number? ')
    params['emergency_contact'] = input('Emergency Contact? ')
    params['emergency_phone'] = input('Emergency Phone? ')

    if input('Do you want to assign a primary care doctor (Y/N)? ').lower() in ('y', 'yes'):
        params['primary_care_doctor'] = pick_primary_care_doctor()

    new_patient = db.Patient(**params)
    new_patient.save()


def add_procedure():
    """User Interface for adding a new procedure to the database."""
    params = dict()
    params['name'] = input("Name? ")
    while True:
        try:
            params['min_cost'] = float(input('Minimum Cost? '))
        except (IndexError, ValueError):
            print('Please input a number')
        else:
            break
    while True:
        try:
            params['max_cost'] = input("Maximum Cost? ")
        except (IndexError, ValueError):
            print('Please input a number')
        else:
            break

    if input('Do you want to assign a pre procedure checklist (Y/N)? ').lower() in ('y', 'yes'):
        params['pre_procedure_checklist'] = input("Checklist: ")

    new_procedure = db.Procedure(**params)
    new_procedure.save()


def add_performed_procedure():
    """User Interface for adding a new performed procedure to the database."""
    params = dict()
    params['patient'] = pick_patient()
    params['doctor'] = pick_primary_care_doctor()
    params['procedure'] = pick_procedure()
    params['procedure_date'] = input('Date of procedure (MM/DD/YYYY)? ')
    if input('Do you want to assign notes (Y/N)? ').lower() in ('y', 'yes'):
        params['notes'] = input('Notes: ')

    new_performed_procedure = db.PerformedProcedure(**params)
    new_performed_procedure.save()


def add_medication():
    """User Interface for adding a new medication to the database."""
    params = dict()
    params['name'] = input("Name? ")
    params['common_name'] = input("Common name? ")

    if input('Do you want to add notes (Y/N)? ').lower() in ('y', 'yes'):
        params['notes'] = input("Checklist: ")

    new_medication = db.Medication(**params)
    new_medication.save()


def add_assigned_medication():
    """User Interface for adding a new applied medication to the database."""
    params = dict()
    params['patient'] = pick_patient()
    params['medication'] = pick_medication()
    params['dosage'] = input('Dosage? ')
    params['date_added'] = input('Date Added (MM/DD/YYYY)? ')
    if input('Do you want to assign notes (Y/N)? ').lower() in ('y', 'yes'):
        params['notes'] = input('Notes: ')

    new_assigned_medication = db.AssignedMedication(**params)
    new_assigned_medication.save()


def pick_procedure():
    """User interface for selecting a procedure."""
    pro_name = input('Identify a procedure by name or press enter to display all procedures? ')
    if pro_name:
        pros = db.Procedure.select().where(db.Procedure.name == pro_name)
    else:
        pros = db.Procedure.select()
    if pros.count() > 1:
        for i, pro in enumerate(pros):
            print(f'{i}. {str(pro)}')
        while True:
            pro_choice = input('Choose by number? ')
            try:
                return pros[int(pro_choice)]
            except (IndexError, ValueError):
                print('Invalid choice')
    elif pros.count() == 1:
        print('Only one matching procedure found')
        print(f'Assigning {str(pros[0])} as procedure')
        return pros[0]
    else:
        print('No procedure found with that name.')
        if input('Skip choosing procedure (Y/N)').lower() in ('y', 'yes'):
            return None
        return pick_patient()


def pick_patient(assign=True):
    """User interface for selecting a patient."""
    pat_name = input('Identify a patient by last name or press enter to display all patients? ')
    if pat_name:
        pats = db.Patient.select().where(db.Patient.last_name == pat_name)
    else:
        pats = db.Patient.select()
    if pats.count() > 1:
        for i, pat in enumerate(pats):
            print(f'{i}. {str(pat)}')
        while True:
            pat_choice = input('Choose by number? ')
            try:
                return pats[int(pat_choice)]
            except (IndexError, ValueError):
                print('Invalid choice')
    elif pats.count() == 1:
        print('Only one matching Patient found')
        if assign:
            print(f'Assigning {str(pats[0])} as patient')
        return pats[0]
    else:
        print('No patient found with that name.')
        if input('Skip choosing patient (Y/N)').lower() in ('y', 'yes'):
            return None
        return pick_patient()


def pick_primary_care_doctor():
    """User Interface for selecting a primary care doctor."""
    doc_name = input('Identify a Doctor by last name or press enter to display all doctors? ')
    if doc_name:
        docs = db.Doctor.select().where(db.Doctor.last_name == doc_name)
    else:
        docs = db.Doctor.select()
    if docs.count() > 1:
        for i, doc in enumerate(docs):
            print(f'{i}. Dr. {doc.first_name} {doc.last_name}')
        while True:
            doc_choice = input('Choose by number? ')
            try:
                return docs[int(doc_choice)]
            except (IndexError, ValueError):
                print('Invalid choice')
    elif docs.count() == 1:
        print('Only one matching Doctor found')
        print(f'Assigning Dr. {docs[0].first_name} {docs[0].last_name} to patient')
        return docs[0]
    else:
        print('No doctor found with that name.')
        if input('Skip choosing primary care doctor (Y/N)').lower() in ('y', 'yes'):
            return None
        return pick_primary_care_doctor()


def pick_medication():
    """User Interface for selecting a medication."""
    med_name = input('Identify medication by name, common name, or press enter to display all medications? ')
    if med_name:
        if db.Medication.select().where(db.Medication.name == med_name):
            meds = db.Medication.select().where(db.Medication.name == med_name)
        else:
            meds = db.Medication.select().where(db.Medication.common_name == med_name)
    else:
        meds = db.Medication.select()
    if meds.count() > 1:
        for i, med in enumerate(meds):
            print(f'{i}. {med.name}')
        while True:
            med_choice = input('Choose by number? ')
            try:
                return meds[int(med_choice)]
            except (IndexError, ValueError):
                print('Invalid choice')
    elif meds.count() == 1:
        print('Only one matching medication found')
        print(f'Assigning {meds[0].name} to patient')
        return meds[0]
    else:
        print('No medications found with that name.')
        if input('Skip choosing medications (Y/N)').lower() in ('y', 'yes'):
            return None
        return pick_medication()


def patient_lookup():
    """User Interface for looking up a patient."""
    pat = pick_patient(assign=False)
    print('\n' + pat.all_info())
    if pat.primary_care_doctor != '':
        print(pat.primary_care_doctor.all_info())
    for procedure in pat.procedure_history:
        print(procedure.all_info())
    for medication in pat.medication_history:
        print(medication.all_info())


def end_program():
    """Exit the program."""
    sys.exit()


menu_dict = {'1': add_doctor,
             '2': add_patient,
             '3': add_procedure,
             '4': add_performed_procedure,
             '5': patient_lookup,
             '6': add_medication,
             '7': add_assigned_medication,
             '8': end_program}

while True:
    user_choice = input(menu)
    if user_choice in menu_dict and menu_dict[user_choice]:
        menu_dict[user_choice]()
    else:
        print('Not a valid choice')

"""User Interface for medical database

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
    """User Interface for adding a new doctor to the database.
    """
    params = dict()
    params['first_name'] = input('First Name? ')
    params['last_name'] = input('Last Name? ')
    params['primary_office'] = input('Primary Office? ')
    new_doc = db.Doctor(**params)
    new_doc.save()


def add_patient():
    """User Interface for adding a new patient to the database.
    """
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
    params['min_cost'] = input("Minimum Cost? ")
    params['max_cost'] = input("Maximum Cost? ")

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


def pick_procedure():
    pro_name = input('Identify a procedure by name or press enter to display all procedures? ')
    if pro_name:
        pros = db.Procedure.select().where(db.Procedure.name == pro_name)
    else:
        pros = db.Procedure.select()
    if pros.count() > 1:
        for i, pat in enumerate(pros):
            print(f'{i}. {str(pro)}')
        while True:
            pro_choice = input('Choose by number? ')
            try:
                return pros[int(pro_choice)]
            except (IndexError, ValueError):
                print('Invalid choice')
    elif pros.count() == 1:
        print('Only one matching procedure found')
        print(f'Assigning {str(pro)} as procedure')
        return pros[0]
    else:
        print('No procedure found with that name.')
        if input('Skip choosing procedure (Y/N)').lower() in ('y', 'yes'):
            return None
        return pick_patient()


def pick_patient(assign=True):
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
            print(f'Assigning {str(pat)} as patient')
        return pats[0]
    else:
        print('No patient found with that name.')
        if input('Skip choosing patient (Y/N)').lower() in ('y', 'yes'):
            return None
        return pick_patient()


def pick_primary_care_doctor():
    """User Interface for selecting a primary care doctor.

    Return: A Doctor object.  Returns None if no doctor selected.
    """
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


def patient_lookup():
    """User Interface for looking up a patient."""
    pat = pick_patient(assign=False)
    print('\n' + pat.all_info())
    if pat.primary_care_doctor != '':
        print(pat.primary_care_doctor.all_info())

def end_program():
    """Exit the program"""
    sys.exit()


menu_dict = {'1': add_doctor,
             '2': add_patient,
             '3': add_procedure,
             '4': add_performed_procedure,
             '5': patient_lookup,
             '6': None,
             '7': None,
             '8': end_program}

while True:
    user_choice = input(menu)
    if user_choice in menu_dict and menu_dict[user_choice]:
        menu_dict[user_choice]()
    else:
        print('Not a valid choice')



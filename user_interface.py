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

    new_doc = db.Patient(**params)
    new_doc.save()


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
                return(docs[int(doc_choice)])
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

def end_program():
    """Exit the program"""
    sys.exit()


menu_dict = {'1': add_doctor,
             '2': add_patient,
             '3': None,
             '4': None,
             '5': None,
             '6': None,
             '7': None,
             '8': end_program}

while True:
    user_choice = input(menu)
    if user_choice in menu_dict and menu_dict[user_choice]:
        menu_dict[user_choice]()
    else:
        print('Not a valid choice')



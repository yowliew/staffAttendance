import time
import datetime
import hashlib
from common.pyfingerprint import PyFingerprint
from common.pyfingerprint import FINGERPRINT_CHARBUFFER1
from common.pyfingerprint import FINGERPRINT_CHARBUFFER2
from flask_socketio import emit
from decimal import Decimal

from models.employees import EFingerModel, EmployeeModel, AttModel, EClassModel


# Enrolls new finger
def enroll(emp_name, namespace):
    # Tries to initialize the sensor
    try:
        f = PyFingerprint('/dev/ttyUSB0', 57600, 0xFFFFFFFF, 0x00000000)

        if not f.verifyPassword():
            raise ValueError('The given fingerprint sensor password is wrong!')

    except Exception as e:
        emit("server_finger_message", "The fingerprint sensor could not be initialized!", namespace=namespace)
        print("The fingerprint sensor could not be initialized!")
        emit("server_finger_message", "Exception message: " + str(e), namespace=namespace)
        print("Exception message: " + str(e))
        emit("server_finger_completed", "Cannot find the Device or Password not correct.", namespace=namespace)
        exit(1)

    # Gets some sensor information
    template_count = str(f.getTemplateCount())
    storage_capacity = str(f.getStorageCapacity())

    emit("server_finger_message", "Currently used templates: " + template_count + "/" + storage_capacity,
        namespace=namespace)
    print('Currently used templates: ' + template_count + '/' + storage_capacity)

    # Tries to enroll new finger
    try:
        emit("server_finger_message", "Waiting for finger...", namespace=namespace)
        print('Waiting for finger...')

        # Wait that finger is read
        while not f.readImage():
            pass

        # Converts read image to characteristics and stores it in charbuffer 1
        f.convertImage(FINGERPRINT_CHARBUFFER1)

        # Checks if finger is already enrolled
        result = f.searchTemplate()
        positionNumber = result[0]

        if positionNumber >= 0:
            emit("server_finger_message", "Template already exists at position #: " + str(positionNumber),
                namespace=namespace)
            print('Template already exists at position #' + str(positionNumber))
            exit(0)

        emit("server_finger_message", "Remove finger...", namespace=namespace)
        print('Remove finger...')
        time.sleep(1)

        emit("server_finger_message", "Waiting for same finger again...", namespace=namespace)
        print('Waiting for same finger again...')

        # Wait that finger is read again
        while not f.readImage():
            pass

        # Converts read image to characteristics and stores it in charbuffer 2
        f.convertImage(FINGERPRINT_CHARBUFFER2)

        # Compares the charbuffers
        if f.compareCharacteristics()==0:
            raise Exception('Fingers do not match')

        # Creates a template
        f.createTemplate()

        # Saves template at new position number
        positionNumber = f.storeTemplate()

        f.loadTemplate(positionNumber, FINGERPRINT_CHARBUFFER2)
        # Downloads the characteristics of template loaded in charbuffer 2
        characterics = str(f.downloadCharacteristics(FINGERPRINT_CHARBUFFER2)).encode('utf-8')
        # Hashes characteristics of template
        hash_val = hashlib.sha256(characterics).hexdigest()

        employee = EmployeeModel.find_by_name(emp_name)
        if employee:
            emp_id = employee.emp_id
            employee_finger = EFingerModel(emp_id, hash_val, positionNumber, 'Y')
            employee_finger.save_to_db()

            emit("server_finger_message", "Finger enrolled successfully!", namespace=namespace)
            print('Finger enrolled successfully!')
            emit("server_finger_message", "New template position #: " + str(positionNumber), namespace=namespace)
            print('New template position #' + str(positionNumber))
            emit("server_finger_completed", "Finger Committed to Database.", namespace=namespace)

    except Exception as e:
        emit("server_finger_message", "Operation failed!", namespace=namespace)
        print('Operation failed!')
        emit("server_finger_message", "Exception message: " + str(e), namespace=namespace)
        print('Exception message: ' + str(e))
        emit("server_finger_completed", "Finger not Committed to Database.", namespace=namespace)
        exit(1)


def report_in_out(emp_name, namespace):
    # Tries to initialize the sensor
    try:
        f = PyFingerprint('/dev/ttyUSB0', 57600, 0xFFFFFFFF, 0x00000000)

        if not f.verifyPassword():
            raise ValueError('The given fingerprint sensor password is wrong!')

    except Exception as e:
        emit("server_finger_message", "The fingerprint sensor could not be initialized!", namespace=namespace)
        print('The fingerprint sensor could not be initialized!')
        emit("server_finger_message", "Exception message: " + str(e), namespace=namespace)
        print('Exception message: ' + str(e))
        emit("server_finger_completed", "Cannot find the Device or Password not correct.", namespace=namespace)
        exit(1)

    # Gets some sensor information
    template_count = str(f.getTemplateCount())
    storage_capacity = str(f.getStorageCapacity())

    emit("server_finger_message", "Currently used templates: " + template_count + "/" + storage_capacity,
        namespace=namespace)
    print('Currently used templates: ' + str(f.getTemplateCount()) + '/' + str(f.getStorageCapacity()))

    # Tries to search the finger and calculate hash
    try:
        emit("server_finger_message", "Waiting for finger...", namespace=namespace)
        print('Waiting for finger...')

        # Wait that finger is read
        while not f.readImage():
            pass

        # Converts read image to characteristics and stores it in charbuffer 1
        f.convertImage(FINGERPRINT_CHARBUFFER1)

        # Search template
        result = f.searchTemplate()

        positionNumber = result[0]
        accuracyScore = result[1]

        if positionNumber==-1:
            emit("server_finger_message", "No match found!", namespace=namespace)
            print('No match found!')
            exit(0)
        else:
            emit("server_finger_message", "Found template at position #" + str(positionNumber), namespace=namespace)
            print('Found template at position #' + str(positionNumber))
            emit("server_finger_message", "The accuracy score is: " + str(accuracyScore), namespace=namespace)
            print('The accuracy score is: ' + str(accuracyScore))

            # Downloads the characteristics of template loaded in charbuffer 1
            characterics = str(f.downloadCharacteristics(FINGERPRINT_CHARBUFFER1)).encode('utf-8')
            hash_val = hashlib.sha256(characterics).hexdigest()

            create_update_att(positionNumber, hash_val, namespace)

    except Exception as e:
        emit("server_finger_message", "Operation failed!", namespace=namespace)
        print('Operation failed!')
        emit("server_finger_message", "Exception message: " + str(e), namespace=namespace)
        print('Exception message: ' + str(e))
        exit(1)


def create_update_att(positionNumber, hash_val, namespace):
    current_datetime = datetime.datetime.now()

    employee_finger = EFingerModel.find_by_finger_id(positionNumber)
    emp_id = employee_finger.emp_id
    finger_id = employee_finger.finger_id

    employee = EmployeeModel.find_by_id(emp_id)
    if employee:
        emp_class = employee.emp_class
        emp_salary = employee.emp_salary
        e_class = EClassModel.find_by_class(emp_class)
        ot_after = e_class.ot_after
        ot_rate = e_class.ot_rate
        max_working = e_class.max_working
    else:
        raise ValueError("Error in Employee and Employee Class Store.")

    if employee_finger:
        employee_att = AttModel.find_by_emp_id_not_out(emp_id)
        if employee_att:
            # this is check out function for employee
            in_datetime = employee_att.in_date

            duration = current_datetime - in_datetime
            duration_seconds = duration.total_seconds()
            actual_duration = Decimal(duration_seconds / 3600)

            # calculate OT hour and rate
            if actual_duration > ot_after:
                ot_hour = actual_duration - ot_after
                ot_amt = (emp_salary / (31 * max_working)) * ot_hour * ot_rate
            else:
                ot_hour = 0
                ot_amt = 0

            employee_att.out_date = current_datetime
            employee_att.tot_work = actual_duration
            employee_att.ot_hour = ot_hour
            employee_att.ot_amt = ot_amt
            employee_att.save_to_db()

            emit("server_finger_message", "Report Out Completed!", namespace=namespace)
            print("Report Out Completed!")
        else:
            # this is check in for employee
            employee_att = AttModel(emp_id, hash_val, finger_id, current_datetime, None, 0, 0, 0, "Y")
            employee_att.save_to_db()

            emit("server_finger_message", "Report in Completed!", namespace=namespace)
            print("Report in Completed!")
    else:
        raise ValueError('The given fingerprint not found in fingerprint store.')

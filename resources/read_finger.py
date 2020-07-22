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
    f = initialize_device(namespace)
    positionNumber = 1000

    # Gets some sensor information
    template_count = str(f.getTemplateCount())
    storage_capacity = str(f.getStorageCapacity())

    emit_message("Currently used templates: " + template_count + "/" + storage_capacity, namespace)

    count = 1
    while count <= 5:
        try:
            emit_message("Waiting for finger #" + str(count), namespace)

            # Wait that finger is read
            while not f.readImage():
                pass

            # Converts read image to characteristics and stores it in charbuffer 1
            f.convertImage(FINGERPRINT_CHARBUFFER1)
            emit_message("Remove finger...", namespace)
            time.sleep(1.5)

            # Creates a template
            f.createTemplate()

            # Saves template at new position number
            positionNumber = f.storeTemplate()

            f.loadTemplate(positionNumber, FINGERPRINT_CHARBUFFER1)
            # Downloads the characteristics of template loaded in charbuffer 1
            characterics = str(f.downloadCharacteristics(FINGERPRINT_CHARBUFFER1)).encode('utf-8')
            # Hashes characteristics of template
            hash_val = hashlib.sha256(characterics).hexdigest()

            employee = EmployeeModel.find_by_name(emp_name)
            if employee:
                emp_id = employee.emp_id
                employee_finger = EFingerModel(emp_id, hash_val, positionNumber, 'Y')
                employee_finger.save_to_db()

                emit_message("Finger enrolled successfully!", namespace)
                emit_message("New template position #: " + str(positionNumber), namespace)
                emit_message("Finger Committed to Database.", namespace)
                count += 1

        except Exception as e:
            emit_message_error("Operation failed!", namespace)
            emit_message_error("Exception message: " + str(e), namespace)
            emit_message_error("Finger not Committed to Database.", namespace)

            f.deleteTemplate(positionNumber)
            f.__del__()
            exit(1)

    display_message_enroll_done(emp_name, namespace)


# Report In/Out for work
def report_in_out(emp_name, namespace):
    f = initialize_device(namespace)

    # Gets some sensor information
    template_count = str(f.getTemplateCount())
    storage_capacity = str(f.getStorageCapacity())

    emit_message("Currently used templates: " + template_count + "/" + storage_capacity, namespace)

    # Tries to search the finger and calculate hash
    try:
        emit_message("Waiting for finger...", namespace)

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
            emit_message_info("No match found! Try again ...", namespace)
            exit(0)
        else:
            emit_message("Found template at position #" + str(positionNumber), namespace)
            emit_message("The accuracy score is: " + str(accuracyScore), namespace)

            # Downloads the characteristics of template loaded in charbuffer 1
            characterics = str(f.downloadCharacteristics(FINGERPRINT_CHARBUFFER1)).encode('utf-8')
            hash_val = hashlib.sha256(characterics).hexdigest()

            create_update_att(positionNumber, hash_val, namespace)

    except Exception as e:
        emit_message_error("Operation failed!", namespace)
        emit_message_error("Exception message: " + str(e), namespace)
        f.__del__()
        exit(1)


def create_update_att(positionNumber, hash_val, namespace):
    current_datetime = datetime.datetime.now()

    employee_finger = EFingerModel.find_by_finger_id(positionNumber)
    emp_id = employee_finger.emp_id
    finger_id = employee_finger.finger_id

    employee = EmployeeModel.find_by_id(emp_id)
    if employee:
        full_name = employee.full_name
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

            print(in_datetime)
            print(current_datetime)

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

            emit_message("Report Out Completed!", namespace)
            display_message_report_out(full_name, in_datetime, current_datetime, actual_duration, ot_hour, namespace)
        else:
            # this is check in for employee
            employee_att = AttModel(emp_id, hash_val, finger_id, current_datetime, None, 0, 0, 0, "Y")
            employee_att.save_to_db()

            emit_message("Report In Completed!", namespace)
            display_message_report_in(full_name, current_datetime, namespace)
    else:
        raise ValueError('The given fingerprint not found in fingerprint store.')


def display_message_report_in(full_name, in_datetime, namespace):
    json_message = {
        "full_name": full_name,
        "in_datetime": str(in_datetime)
    }
    emit("server_finger_completed_report_in", json_message, namespace=namespace)


def display_message_report_out(full_name, in_datetime, out_datetime, actual_duration, ot_hour, namespace):
    json_message = {
        "full_name": full_name,
        "in_datetime": str(in_datetime),
        "out_datetime": str(out_datetime),
        "actual_duration": str(actual_duration),
        "ot_hour": str(ot_hour)
    }
    emit("server_finger_completed_report_out", json_message, namespace=namespace)


def display_message_enroll_done(full_name, namespace):
    json_message = {
        "full_name": full_name,
        "message": "Thanks. You have completed 5 fingerscans successfully"
    }
    emit("server_finger_completed_enroll", json_message, namespace=namespace)


def emit_message_error(msg, namespace):
    emit("server_finger_message_error", msg, namespace=namespace)
    emit_message(msg, namespace)


def emit_message_info(msg, namespace):
    emit("server_finger_message_info", msg, namespace=namespace)
    emit_message(msg, namespace)


def emit_message(msg, namespace):
    emit("server_finger_message", msg, namespace=namespace)
    print(msg)


def initialize_device(namespace):
    # Tries to initialize the sensor
    try:
        finger_handler = PyFingerprint('/dev/ttyUSB0', 57600, 0xFFFFFFFF, 0x00000000)

        if not finger_handler.verifyPassword():
            raise ValueError('The given fingerprint sensor password is wrong!')

        return finger_handler

    except Exception as e:
        emit_message_error("The fingerprint sensor could not be initialized!", namespace)
        emit_message_error("Exception message: " + str(e), namespace)
        emit_message_error("Cannot find the Device or Password not correct.", namespace)
        exit(1)

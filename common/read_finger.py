import time
import hashlib
from common.pyfingerprint import PyFingerprint
from common.pyfingerprint import FINGERPRINT_CHARBUFFER1
from common.pyfingerprint import FINGERPRINT_CHARBUFFER2

from flask_socketio import emit


# Enrolls new finger

def enroll(namespace):
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
        if f.compareCharacteristics() == 0:
            raise Exception('Fingers do not match')

        # Creates a template
        f.createTemplate()

        # Saves template at new position number
        positionNumber = f.storeTemplate()
        emit("server_finger_message", "Finger enrolled successfully!", namespace=namespace)
        print('Finger enrolled successfully!')
        emit("server_finger_message", "New template position #: " + str(positionNumber), namespace=namespace)
        print('New template position #' + str(positionNumber))

    except Exception as e:
        emit("server_finger_message", "Operation failed!", namespace=namespace)
        print('Operation failed!')
        emit("server_finger_message", "Exception message: " + str(e), namespace=namespace)
        print('Exception message: ' + str(e))
        exit(1)


def report_in_out(namespace):
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

        if positionNumber == -1:
            emit("server_finger_message", "No match found!", namespace=namespace)
            print('No match found!')
            exit(0)
        else:
            emit("server_finger_message", "Found template at position #" + str(positionNumber), namespace=namespace)
            print('Found template at position #' + str(positionNumber))
            emit("server_finger_message", "The accuracy score is: " + str(accuracyScore), namespace=namespace)
            print('The accuracy score is: ' + str(accuracyScore))

        # OPTIONAL stuff
        #

        # Loads the found template to charbuffer 1
        f.loadTemplate(positionNumber, FINGERPRINT_CHARBUFFER1)

        # Downloads the characteristics of template loaded in charbuffer 1
        characterics = str(f.downloadCharacteristics(FINGERPRINT_CHARBUFFER1)).encode('utf-8')

        # Hashes characteristics of template
        emit("server_finger_message", "SHA-2 hash of template: " + hashlib.sha256(characterics).hexdigest(),
             namespace=namespace)
        print('SHA-2 hash of template: ' + hashlib.sha256(characterics).hexdigest())

    except Exception as e:
        emit("server_finger_message", "Operation failed!", namespace=namespace)
        print('Operation failed!')
        emit("server_finger_message", "Exception message: " + str(e), namespace=namespace)
        print('Exception message: ' + str(e))
        exit(1)

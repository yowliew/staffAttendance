from flask_socketio import emit
from pre_app import socketio

import resources.read_finger as scanner


# users = {}


@socketio.on("client_finger_connect", namespace="/finger_namespace")
def get_connected(msg):
    print(msg)
    emit("server_finger_message", msg, namespace="/finger_namespace")


@socketio.on("client_finger_report_in_out", namespace="/finger_namespace")
def get_connected(msg):
    print(msg)
    emit("server_finger_message", msg, namespace="/finger_namespace")
    scanner.report_in_out(msg, namespace="/finger_namespace")


@socketio.on("client_finger_enroll", namespace="/finger_namespace")
def get_enroll(msg):
    print("Enroll fingerprint for " + msg)
    emit("server_finger_message", "Enroll fingerprint for " + msg, namespace="/finger_namespace")
    scanner.enroll(msg, namespace="/finger_namespace")

# @socketio.on("client_finger_login", namespace="/finger_namespace")
# def send_receive_msg(msg):
#     users[msg] = request.sid
#     print(users)
#
#
# @socketio.on("client_finger_message", namespace="/finger_namespace")
# def send_private(pay_load):
#     the_session = users[pay_load["username"]]
#     emit("server_finger_message", pay_load["message"], room=the_session)
#
#
# def server_send(the_msg):
#     emit("server_finger_message", the_msg, namespace="/finger_namespace", broadcast=True)
